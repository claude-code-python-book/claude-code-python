import asyncio
import time

import pytest

from notify.summary import OrderNotFoundError, optional, order_summary
from tests.conftest import ORDER, FakeServices

pytestmark = pytest.mark.anyio


async def test_the_calls_overlap() -> None:
    services = FakeServices(delay=0.2)
    start = time.perf_counter()
    summary = await order_summary(services, ORDER.id)
    elapsed = time.perf_counter() - start
    assert summary.delivery == "Thursday 19 November" and summary.points == 1320
    # order and delivery run together, then points: two rounds, not three
    assert 0.38 < elapsed < 0.55


async def test_a_slow_extra_is_cut_off() -> None:
    services = FakeServices(delay=0.05, delivery_delay=5)
    start = time.perf_counter()
    summary = await order_summary(services, ORDER.id, extras_timeout=0.3)
    assert summary.delivery is None
    assert summary.points == 1320
    assert time.perf_counter() - start < 0.5
    assert services.cancelled == ["delivery"]


async def test_a_failing_extra_falls_back() -> None:
    summary = await order_summary(FakeServices(delay=0.01, fail={"points"}), ORDER.id)
    assert summary.points is None and summary.delivery is not None


async def test_a_missing_order_cancels_the_rest() -> None:
    services = FakeServices(delay=0.05, delivery_delay=5)
    with pytest.RaisesGroup(OrderNotFoundError):
        await order_summary(services, 999)
    assert services.cancelled == ["delivery"]


async def test_optional_does_not_swallow_cancellation() -> None:
    task = asyncio.create_task(optional(asyncio.sleep(5), seconds=10))
    await asyncio.sleep(0.01)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
