async def test_a_slow_extra_is_cut_off() -> None:
    services = FakeServices(delay=0.05, delivery_delay=5)
    start = time.perf_counter()
    summary = await order_summary(services, ORDER.id, extras_timeout=0.3)
    assert summary.delivery is None
    assert summary.points == 1320
    assert time.perf_counter() - start < 0.5
    assert services.cancelled == ["delivery"]


async def test_a_missing_order_cancels_the_rest() -> None:
    services = FakeServices(delay=0.05, delivery_delay=5)
    with pytest.RaisesGroup(OrderNotFoundError):
        await order_summary(services, 999)
    assert services.cancelled == ["delivery"]
