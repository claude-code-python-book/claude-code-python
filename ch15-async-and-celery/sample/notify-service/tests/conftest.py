import asyncio
from collections.abc import Iterator
from dataclasses import dataclass, field
from decimal import Decimal

import pytest

from notify.summary import Order, OrderNotFoundError
from tests.resp import MiniRedis

ORDER = Order(
    id=1042,
    email="asha@example.com",
    name="Asha",
    total=Decimal("68.50"),
    lines=(
        ("Ceramic mug", 2, Decimal("12.25")),
        ("Pour-over kettle", 1, Decimal("44.00")),
    ),
)


@dataclass
class FakeServices:
    """The three services, with delays and failures you can set per test."""

    delay: float = 0.1
    delivery_delay: float | None = None
    fail: set[str] = field(default_factory=set)
    cancelled: list[str] = field(default_factory=list)

    async def _wait(self, name: str, seconds: float) -> None:
        try:
            await asyncio.sleep(seconds)
        except asyncio.CancelledError:
            self.cancelled.append(name)
            raise
        if name in self.fail:
            raise ConnectionError(f"{name} is down")

    async def order(self, order_id: int) -> Order:
        await self._wait("order", self.delay)
        if order_id != ORDER.id:
            raise OrderNotFoundError(order_id)
        return ORDER

    async def delivery_estimate(self, order_id: int) -> str:
        await self._wait("delivery", self.delivery_delay or self.delay)
        return "Thursday 19 November"

    async def loyalty_points(self, email: str) -> int:
        await self._wait("points", self.delay)
        return 1320


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def redis() -> Iterator[MiniRedis]:
    """A real Redis connection on database 15, emptied before and after."""
    try:
        client = MiniRedis(db=15)
    except OSError:
        pytest.skip("Redis is not running on localhost:6379")
    client.flushdb()
    yield client
    client.flushdb()
    client.close()
