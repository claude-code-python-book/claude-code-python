import asyncio
import logging
import time

logging.basicConfig(level=logging.WARNING, format="%(levelname)s:%(name)s:%(message)s")


async def send_receipt(order_id: int) -> None:
    time.sleep(0.25)  # a blocking SMTP call hiding in an async path


async def main() -> None:
    await send_receipt(1042)


asyncio.run(main(), debug=True)
