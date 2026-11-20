"""Budget stops, crashes, schema validation, and the shadowing warning."""

import warnings
from pathlib import Path

import pytest
from claude_agent_sdk import CanUseToolShadowedWarning, ProcessError

from reviewbot.agent import run_review

from fakecli import FakeCLI
from script import assistant, mcp_call, mcp_handshake, result, tool_use

FINDING = {"path": "stats.py", "line": 2, "severity": "major", "message": "x"}


@pytest.mark.anyio
async def test_budget_stop_keeps_partial_findings(repo: Path) -> None:
    turn = [
        *mcp_handshake("review"),
        assistant([tool_use("t1", "mcp__review__record_finding", FINDING)], "m1"),
        mcp_call("review", 1, "record_finding", FINDING),
        result("", subtype="error_max_budget_usd", is_error=True, cost=0.51),
    ]
    # The real CLI exits non-zero after an error result; the SDK then
    # raises ResultError, which run_review() catches.
    report = await run_review(repo, transport=FakeCLI([turn], exit_code=1))
    assert report.subtype == "error_max_budget_usd"
    assert len(report.findings) == 1
    assert report.cost_usd == pytest.approx(0.51)


@pytest.mark.anyio
async def test_crash_before_any_result_raises(repo: Path) -> None:
    with pytest.raises(ProcessError):
        await run_review(repo, transport=FakeCLI([[]], exit_code=1))


@pytest.mark.anyio
async def test_schema_rejects_unknown_severity(repo: Path) -> None:
    bad = {**FINDING, "severity": "blocker"}
    cli = FakeCLI([[*mcp_handshake("review"),
                    mcp_call("review", 1, "record_finding", bad, "r1"),
                    result("done")]])
    report = await run_review(repo, transport=cli)
    rpc = cli.answers["r1"]["response"]["mcp_response"]["result"]
    assert rpc["isError"] is True
    assert "is not one of" in rpc["content"][0]["text"]
    assert report.findings == []          # the handler never ran


@pytest.mark.anyio
async def test_invalid_base_is_rejected_before_spawning(repo: Path) -> None:
    with pytest.raises(ValueError, match="invalid base"):
        await run_review(repo, "--upload-pack=evil", transport=FakeCLI([]))


@pytest.mark.anyio
async def test_sdk_warns_that_allowed_tools_skip_the_callback(repo: Path) -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        await run_review(repo, transport=FakeCLI([[result("ok")]]))
    shadowed = [w for w in caught if w.category is CanUseToolShadowedWarning]
    assert "mcp__review__record_finding" in str(shadowed[0].message)
