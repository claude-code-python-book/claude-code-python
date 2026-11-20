import asyncio
import time


async def fetch_estimate_badly() -> str:
    try:
        await asyncio.sleep(5)  # a slow shipping service
        return "Thursday"
    except BaseException:  # catches CancelledError too
        return "unknown"


async def fetch_estimate() -> str:
    try:
        await asyncio.sleep(5)
        return "Thursday"
    except Exception:  # CancelledError is a BaseException: it passes through
        return "unknown"


async def main() -> None:
    for fetch in (fetch_estimate_badly, fetch_estimate):
        start = time.perf_counter()
        try:
            async with asyncio.timeout(0.2):
                result = await fetch()
            print(f"{fetch.__name__:<22} returned {result!r}")
        except TimeoutError:
            print(f"{fetch.__name__:<22} raised TimeoutError")
        print(f"{'':<22} after {time.perf_counter() - start:.2f} s")


asyncio.run(main())
