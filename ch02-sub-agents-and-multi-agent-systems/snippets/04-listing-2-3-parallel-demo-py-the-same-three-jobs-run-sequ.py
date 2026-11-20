"""Sequential vs parallel: three fake 'agents' that each take 2 seconds."""
import asyncio
import time

async def fake_agent(name: str, seconds: float) -> str:
    await asyncio.sleep(seconds)        # stands in for a slow API call
    return f"{name} done"

async def sequential() -> list[str]:
    # Each await finishes before the next one starts.
    return [
        await fake_agent("security", 2),
        await fake_agent("tests", 2),
        await fake_agent("style", 2),
    ]

async def parallel() -> list[str]:
    # gather() starts all three at once and waits for every one.
    results = await asyncio.gather(
        fake_agent("security", 2),
        fake_agent("tests", 2),
        fake_agent("style", 2),
    )
    return list(results)

for run in (sequential, parallel):
    start = time.perf_counter()
    results = asyncio.run(run())
    print(f"{run.__name__:<10} {time.perf_counter() - start:.1f}s  {results}")
