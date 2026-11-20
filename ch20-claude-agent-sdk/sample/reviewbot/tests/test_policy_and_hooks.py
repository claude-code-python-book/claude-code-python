"""The permission callback and hook callbacks are plain coroutines too."""

from pathlib import Path

import pytest
from claude_agent_sdk import (
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)

from reviewbot.hooks import AuditLog, block_secrets, looks_secret
from reviewbot.policy import make_policy

CTX = ToolPermissionContext()


@pytest.mark.anyio
async def test_policy_allows_reads_inside_repo(repo: Path) -> None:
    policy = make_policy(repo)
    decision = await policy("Read", {"file_path": str(repo / "stats.py")}, CTX)
    assert isinstance(decision, PermissionResultAllow)


@pytest.mark.anyio
@pytest.mark.parametrize("tool,args", [
    ("Read", {"file_path": "/etc/passwd"}),
    ("Grep", {"pattern": "TOKEN", "path": "../.."}),
    ("Bash", {"command": "rm -rf build"}),
    ("Write", {"file_path": "stats.py", "content": ""}),
])
async def test_policy_denies_everything_else(repo: Path, tool: str,
                                             args: dict) -> None:
    decision = await make_policy(repo)(tool, args, CTX)
    assert isinstance(decision, PermissionResultDeny)
    assert decision.message


@pytest.mark.parametrize("value,secret", [
    (".env", True), ("config/.env.production", True), ("certs/server.pem", True),
    ("/home/u/.ssh/id_rsa", True), ("settings.py", False), ("env.py", False),
])
def test_looks_secret(value: str, secret: bool) -> None:
    assert looks_secret(value) is secret


@pytest.mark.anyio
async def test_block_secrets_denies_and_explains() -> None:
    out = await block_secrets(
        {"hook_event_name": "PreToolUse", "tool_name": "Read",
         "tool_input": {"file_path": ".env"}}, "t1", {"signal": None})
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert await block_secrets(
        {"hook_event_name": "PreToolUse", "tool_name": "Read",
         "tool_input": {"file_path": "stats.py"}}, "t2", {"signal": None}) == {}


@pytest.mark.anyio
async def test_audit_log_writes_jsonl(tmp_path: Path) -> None:
    log = AuditLog(tmp_path / "audit.jsonl")
    await log({"hook_event_name": "PostToolUse", "session_id": "s",
               "tool_name": "Read", "tool_input": {"file_path": "a.py"}},
              "t9", {"signal": None})
    line = (tmp_path / "audit.jsonl").read_text().strip()
    assert '"tool": "Read"' in line and '"tool_use_id": "t9"' in line
