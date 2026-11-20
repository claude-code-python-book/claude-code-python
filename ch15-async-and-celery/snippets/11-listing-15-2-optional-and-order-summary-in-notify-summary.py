async def optional[T](call: Awaitable[T], seconds: float) -> T | None:
    """Return the call's result, or None if it fails or takes too long.

    CancelledError is not caught: if the whole summary is cancelled, this
    call must stop too.
    """
    try:
        async with asyncio.timeout(seconds):
            return await call
    except Exception:  # noqa: BLE001 - a missing extra must never stop the email
        return None


async def order_summary(
    services: Services, order_id: int, extras_timeout: float = 0.5
) -> Summary:
    """Load the order, the delivery estimate and the points concurrently.

    Raises:
        ExceptionGroup: If loading the order fails; the others are cancelled.
    """
    async with asyncio.TaskGroup() as tg:
        order_task = tg.create_task(services.order(order_id))
        delivery = tg.create_task(
            optional(services.delivery_estimate(order_id), extras_timeout)
        )
        order = await order_task  # the points lookup needs the email address
        points = tg.create_task(
            optional(services.loyalty_points(order.email), extras_timeout)
        )
    return Summary(order, delivery.result(), points.result())
