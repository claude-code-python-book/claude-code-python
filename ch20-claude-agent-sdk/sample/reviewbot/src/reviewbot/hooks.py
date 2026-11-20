"""Hook callbacks: a secrets guard before tools run, an audit log after."""

from __future__ import annotations

import json
import time
from fnmatch import fnmatch
from pathlib import Path, PurePosixPath
from typing import Any, cast

from claude_agent_sdk import HookContext, HookInput, HookJSONOutput, HookMatcher
from claude_agent_sdk.types import HookEvent

SECRET_GLOBS = (".env", ".env.*", "*.pem", "*.key", "id_rsa*")


def looks_secret(value: str) -> bool:
    name = PurePosixPath(value).name
    return any(fnmatch(name, pattern) for pattern in SECRET_GLOBS)


async def block_secrets(
    input_data: HookInput, tool_use_id: str | None, context: HookContext
) -> HookJSONOutput:
    data = cast(dict[str, Any], input_data)
    values = [v for v in data["tool_input"].values() if isinstance(v, str)]
    if any(looks_secret(v) for v in values):
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Secret files are off limits.",
            }
        }
    return {}


class AuditLog:
    """Collects one JSON record per completed tool call."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path
        self.records: list[dict[str, Any]] = []

    async def __call__(
        self, input_data: HookInput, tool_use_id: str | None, context: HookContext
    ) -> HookJSONOutput:
        data = cast(dict[str, Any], input_data)
        record = {
            "ts": round(time.time(), 3),
            "session": data.get("session_id"),
            "tool": data.get("tool_name"),
            "tool_use_id": tool_use_id,
            "input": data.get("tool_input"),
        }
        self.records.append(record)
        if self.path is not None:
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(record) + "\n")
        return {}


def review_hooks(audit: AuditLog) -> dict[HookEvent, list[HookMatcher]]:
    return {
        "PreToolUse": [HookMatcher(matcher="Read|Grep|Glob", hooks=[block_secrets])],
        "PostToolUse": [HookMatcher(hooks=[audit])],
    }
