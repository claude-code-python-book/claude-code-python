"""In-process MCP tools that give the review agent a narrow view of git."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    McpSdkServerConfig,
    SdkMcpTool,
    ToolAnnotations,
    create_sdk_mcp_server,
    tool,
)

MAX_DIFF_CHARS = 12_000
SEVERITIES = ("info", "minor", "major", "critical")


@dataclass
class Finding:
    path: str
    line: int
    severity: str
    message: str


@dataclass
class ReviewState:
    repo: Path
    base: str
    findings: list[Finding] = field(default_factory=list)


def text(body: str, *, error: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {"content": [{"type": "text", "text": body}]}
    if error:
        result["is_error"] = True
    return result


async def git(repo: Path, *args: str) -> tuple[int, str]:
    proc = await asyncio.create_subprocess_exec(
        "git", "-C", str(repo), *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    out, _ = await proc.communicate()
    return proc.returncode or 0, out.decode("utf-8", "replace")


def safe_path(repo: Path, rel: str) -> str | None:
    """Return rel if it names a file inside repo, else None."""
    if not rel or rel.startswith("-") or Path(rel).is_absolute():
        return None
    resolved = (repo / rel).resolve()
    return rel if resolved.is_relative_to(repo.resolve()) else None


def review_tools(state: ReviewState) -> list[SdkMcpTool[Any]]:
    read_only = ToolAnnotations(readOnlyHint=True)

    @tool("changed_files", "List files changed since the base branch.",
          {}, annotations=read_only)
    async def changed_files(args: dict[str, Any]) -> dict[str, Any]:
        code, out = await git(state.repo, "diff", "--name-only",
                              f"{state.base}...HEAD")
        if code != 0:
            return text(f"git diff failed: {out.strip()}", error=True)
        return text(out.strip() or "(no changes)")

    @tool("file_diff", "Show the diff of one changed file.",
          {"path": str}, annotations=read_only)
    async def file_diff(args: dict[str, Any]) -> dict[str, Any]:
        rel = safe_path(state.repo, args["path"])
        if rel is None:
            return text(f"Refusing path {args['path']!r}", error=True)
        code, out = await git(state.repo, "diff", f"{state.base}...HEAD",
                              "--", rel)
        if code != 0:
            return text(f"git diff failed: {out.strip()}", error=True)
        if len(out) > MAX_DIFF_CHARS:
            out = out[:MAX_DIFF_CHARS] + "\n[diff truncated]"
        return text(out or "(no diff for this path)")

    @tool("record_finding", "Record one review finding.", {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "line": {"type": "integer", "minimum": 1},
            "severity": {"type": "string", "enum": list(SEVERITIES)},
            "message": {"type": "string", "minLength": 1},
        },
        "required": ["path", "line", "severity", "message"],
    })
    async def record_finding(args: dict[str, Any]) -> dict[str, Any]:
        if safe_path(state.repo, args["path"]) is None:
            return text(f"Unknown path {args['path']!r}", error=True)
        state.findings.append(Finding(args["path"], args["line"],
                                      args["severity"], args["message"]))
        return text(f"Recorded finding #{len(state.findings)}")

    return [changed_files, file_diff, record_finding]


def build_review_server(state: ReviewState) -> McpSdkServerConfig:
    return create_sdk_mcp_server(name="review", version="1.0.0",
                                 tools=review_tools(state))


REVIEW_TOOLS = [
    "mcp__review__changed_files",
    "mcp__review__file_diff",
    "mcp__review__record_finding",
]
