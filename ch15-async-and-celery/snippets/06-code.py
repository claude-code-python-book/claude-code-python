import asyncio
import subprocess
import time

import requests


async def order_page(order_id: int) -> dict:
    response = requests.get(f"https://orders.internal/orders/{order_id}", timeout=5)
    with open(f"/var/cache/orders/{order_id}.json") as cache:
        cached = cache.read()
    time.sleep(0.1)  # "give the cache a moment"
    subprocess.run(["./warm-cache", str(order_id)], check=True)
    return {"order": response.json(), "cached": cached}


async def place_order(order_id: int) -> None:
    asyncio.create_task(notify_warehouse(order_id))


async def notify_warehouse(order_id: int) -> None: ...
