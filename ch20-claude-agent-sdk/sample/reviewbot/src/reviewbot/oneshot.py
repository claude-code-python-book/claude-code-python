"""One-shot question answering over a repository with query()."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    Transport,
    query,
)


async def ask_repo(
    repo: Path, question: str, *, transport: Transport | None = None
) -> str:
    options = ClaudeAgentOptions(
        cwd=repo,
        tools=["Read", "Grep", "Glob"],   # read-only built-ins only
        permission_mode="dontAsk",        # anything that would prompt: denied
        setting_sources=[],
        max_turns=8,
    )
    answer = ""
    async for message in query(prompt=question, options=options,
                               transport=transport):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    print(f"  -> {block.name} {block.input}", file=sys.stderr)
                elif isinstance(block, TextBlock):
                    answer = block.text
        elif isinstance(message, ResultMessage):
            print(f"  ({message.subtype}, {message.num_turns} turns, "
                  f"~${message.total_cost_usd or 0:.4f})", file=sys.stderr)
            answer = message.result or answer
    return answer


if __name__ == "__main__":
    print(asyncio.run(ask_repo(Path.cwd(), " ".join(sys.argv[1:]))))
