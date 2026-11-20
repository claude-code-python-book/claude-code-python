"""Three reviewer sub-agents look at the same file at the same time."""
import asyncio
import sys
from pathlib import Path

import anthropic

MODEL = "claude-sonnet-5-5"
client = anthropic.AsyncAnthropic()      # the async client works with await

ASPECTS = ["security", "performance", "readability"]

async def review(aspect: str, code: str) -> tuple[str, str]:
    """One sub-agent that reviews the code for a single aspect only."""
    response = await client.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=f"You review Python code for {aspect} problems only. "
               "List at most three issues, most serious first. "
               "If you find none, say so.",
        messages=[{"role": "user", "content": code}],
    )
    return aspect, "".join(b.text for b in response.content if b.type == "text")

async def main() -> None:
    code = Path(sys.argv[1]).read_text(encoding="utf-8")
    results = await asyncio.gather(*(review(a, code) for a in ASPECTS))
    for aspect, findings in results:          # gather keeps the input order
        print(f"=== {aspect} ===\n{findings}\n")

asyncio.run(main())
