import asyncio
import os

from claude_agent_sdk import ClaudeAgentOptions, query


async def main() -> None:
    options = ClaudeAgentOptions(
        cwd=os.getcwd(),                      # .claude/skills/ here or above
        setting_sources=["user", "project"],  # load skills from disk
        skills="all",                         # allow every discovered skill
        allowed_tools=["Read", "Write", "Bash"],
    )
    async for message in query(prompt="Write tests for src/shop/pricing.py",
                               options=options):
        print(message)


asyncio.run(main())
