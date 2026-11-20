import asyncio


async def notify_warehouse(order_id: int) -> None:
    print(f"warehouse told about order {order_id}")


async def main() -> None:
    notify_warehouse(1042)  # missing await
    print("order placed")


asyncio.run(main())
