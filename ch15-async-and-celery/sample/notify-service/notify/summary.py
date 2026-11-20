"""Gather what a confirmation email needs, from three services at once.

The order itself is required: if it can't be loaded, there is no email.
The delivery estimate and the loyalty balance are nice to have: each gets
its own time limit and a fallback, so a slow service can't hold up the email.
"""

import asyncio
from collections.abc import Awaitable
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


class OrderNotFoundError(Exception):
    """The order service has no such order."""


@dataclass(frozen=True)
class Order:
    """The parts of an order the email shows."""

    id: int
    email: str
    name: str
    total: Decimal
    lines: tuple[tuple[str, int, Decimal], ...]  # (item, quantity, price)


@dataclass(frozen=True)
class Summary:
    """Everything the confirmation email needs."""

    order: Order
    delivery: str | None  # e.g. "Thursday 19 November", or None if unknown
    points: int | None  # loyalty balance, or None if unknown


class Services(Protocol):
    """The three services the summary reads from."""

    async def order(self, order_id: int) -> Order: ...  # noqa: D102
    async def delivery_estimate(self, order_id: int) -> str: ...  # noqa: D102
    async def loyalty_points(self, email: str) -> int: ...  # noqa: D102


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
