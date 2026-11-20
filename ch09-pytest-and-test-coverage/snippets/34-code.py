@pytest_asyncio.fixture
async def tables(rates_server: str) -> dict[str, dict[str, Decimal]]:
    return await fx.fetch_many(["GBP", "EUR"], rates_server)


@pytest.mark.asyncio
async def test_round_trip_is_close(
    tables: dict[str, dict[str, Decimal]],
) -> None:
    round_trip = tables["GBP"]["EUR"] * tables["EUR"]["GBP"]
    assert abs(round_trip - 1) < Decimal("0.01")
