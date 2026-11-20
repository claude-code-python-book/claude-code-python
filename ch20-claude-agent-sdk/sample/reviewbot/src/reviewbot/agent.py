"""Wire tools, policy, and hooks into one review run."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultError,
    ResultMessage,
    Transport,
    query,
)

from .hooks import AuditLog, review_hooks
from .policy import make_policy
from .tools import REVIEW_TOOLS, Finding, ReviewState, build_review_server

BASE_RE = re.compile(r"^[A-Za-z0-9._/][A-Za-z0-9._/-]{0,99}$")

SYSTEM_PROMPT = """You are a code reviewer for a Python repository.
1. Call changed_files, then file_diff for each changed Python file.
2. Read surrounding code with Read or Grep when a diff needs context.
3. Call record_finding once per real problem: bugs, security issues,
   missing tests for new behaviour. Skip style nits that Ruff would catch.
4. Finish with a two-sentence summary. Never edit files."""


@dataclass
class ReviewReport:
    findings: list[Finding]
    summary: str
    subtype: str
    cost_usd: float
    turns: int
    session_id: str
    audit: list[dict[str, Any]] = field(default_factory=list)


def build_options(state: ReviewState, audit: AuditLog) -> ClaudeAgentOptions:
    return ClaudeAgentOptions(
        cwd=state.repo,
        system_prompt=SYSTEM_PROMPT,
        tools=["Read", "Grep", "Glob"],          # built-ins Claude can see
        mcp_servers={"review": build_review_server(state)},
        allowed_tools=REVIEW_TOOLS,              # run without asking
        can_use_tool=make_policy(state.repo),    # everything else
        hooks=review_hooks(audit),
        setting_sources=[],                      # ignore local settings files
        max_turns=30,
        max_budget_usd=0.50,
    )


async def run_review(
    repo: Path, base: str = "main", *, transport: Transport | None = None
) -> ReviewReport:
    if not BASE_RE.match(base):
        raise ValueError(f"invalid base ref: {base!r}")
    state = ReviewState(repo=repo, base=base)
    audit = AuditLog()
    summary, result = "", None
    try:
        async for message in query(
            prompt=f"Review the changes on this branch against {base}.",
            options=build_options(state, audit),
            transport=transport,
        ):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if hasattr(block, "text"):
                        summary = block.text
            elif isinstance(message, ResultMessage):
                result = message
    except ResultError:
        # query() raises after yielding an error result (budget, max turns).
        # Keep the partial review; re-raise if no result ever arrived.
        if result is None:
            raise
    if result is None:
        raise RuntimeError("the agent ended without a result message")
    return ReviewReport(
        findings=state.findings,
        summary=result.result or summary,
        subtype=result.subtype,
        cost_usd=result.total_cost_usd or 0.0,
        turns=result.num_turns,
        session_id=result.session_id,
        audit=audit.records,
    )
