"""Drive run_review() end to end against a scripted CLI session."""

from pathlib import Path

import pytest

from reviewbot.agent import run_review

from fakecli import FakeCLI
from script import (
    assistant,
    hook,
    init_frame,
    mcp_call,
    mcp_handshake,
    permission,
    result,
    text_block,
    tool_result,
    tool_use,
)

FINDING = {"path": "stats.py", "line": 2, "severity": "major",
           "message": "average() now raises ZeroDivisionError on []"}


def review_turn() -> list[dict]:
    secret, outside = {"file_path": ".env"}, {"file_path": "/etc/passwd"}
    return [
        init_frame(["Read", "Grep", "Glob", "mcp__review__changed_files"]),
        *mcp_handshake("review"),
        assistant([tool_use("t1", "mcp__review__changed_files", {})], "m1"),
        mcp_call("review", 1, "changed_files", {}, "r-changed"),
        hook("hook_1", "PostToolUse", "mcp__review__changed_files", {}, "t1"),
        tool_result("t1", "stats.py"),
        assistant([tool_use("t2", "mcp__review__file_diff",
                            {"path": "stats.py"})], "m2"),
        mcp_call("review", 2, "file_diff", {"path": "stats.py"}, "r-diff"),
        tool_result("t2", "(diff)"),
        assistant([tool_use("t3", "Read", secret)], "m3"),
        hook("hook_0", "PreToolUse", "Read", secret, "t3", "r-guard"),
        tool_result("t3", "Secret files are off limits.", is_error=True),
        assistant([tool_use("t4", "Read", outside)], "m4"),
        hook("hook_0", "PreToolUse", "Read", outside, "t4"),
        permission("Read", outside, "t4", "r-perm"),
        tool_result("t4", "denied", is_error=True),
        assistant([tool_use("t5", "mcp__review__record_finding", FINDING)],
                  "m5"),
        mcp_call("review", 3, "record_finding", FINDING, "r-find"),
        tool_result("t5", "Recorded finding #1"),
        assistant([text_block("One major issue: average() lost its guard.")],
                  "m6"),
        result("One major issue: average() lost its guard.", turns=6),
    ]


def mcp_text(cli: FakeCLI, request_id: str) -> str:
    rpc = cli.answers[request_id]["response"]["mcp_response"]
    return rpc["result"]["content"][0]["text"]


@pytest.mark.anyio
async def test_review_session(repo: Path) -> None:
    cli = FakeCLI([review_turn()])
    report = await run_review(repo, "main", transport=cli)

    # The in-process tools ran for real against the git fixture.
    assert mcp_text(cli, "r-changed") == "stats.py"
    assert "-    if not xs:" in mcp_text(cli, "r-diff")
    assert [f.severity for f in report.findings] == ["major"]

    # The hook blocked the secret; the policy blocked the outside path.
    guard = cli.answers["r-guard"]["response"]["hookSpecificOutput"]
    assert guard["permissionDecision"] == "deny"
    assert cli.answers["r-perm"]["response"]["behavior"] == "deny"

    # Options reached the CLI: hooks registered, prompt sent.
    assert cli.init_request is not None
    assert cli.init_request["hooks"]["PreToolUse"] == [
        {"matcher": "Read|Grep|Glob", "hookCallbackIds": ["hook_0"]}]
    prompt = next(m for m in cli.sent if m["type"] == "user")
    assert "against main" in prompt["message"]["content"]

    assert report.subtype == "success"
    assert report.cost_usd == pytest.approx(0.0123)
    assert [r["tool"] for r in report.audit] == ["mcp__review__changed_files"]
