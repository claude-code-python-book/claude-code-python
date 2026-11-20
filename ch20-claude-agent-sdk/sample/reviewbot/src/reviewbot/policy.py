"""Runtime permission decisions for tool calls nothing else resolved."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    CanUseTool,
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)

READ_TOOLS = {"Read": "file_path", "Grep": "path", "Glob": "path"}


def make_policy(repo: Path) -> CanUseTool:
    root = repo.resolve()

    async def can_use_tool(
        tool_name: str, input_data: dict[str, Any], context: ToolPermissionContext
    ) -> PermissionResultAllow | PermissionResultDeny:
        if tool_name not in READ_TOOLS:
            return PermissionResultDeny(
                message=f"{tool_name} is not available to the review bot."
            )
        raw = input_data.get(READ_TOOLS[tool_name]) or str(root)
        target = (root / raw).resolve()
        if not target.is_relative_to(root):
            return PermissionResultDeny(
                message=f"{raw} is outside the repository; stay inside it."
            )
        return PermissionResultAllow()

    return can_use_tool
