from decimal import Decimal
from urllib.error import HTTPError

import pytest

from invoicer import fx


@pytest.mark.asyncio
async def test_fetch_many_returns_one_table_per_base(rates_server: str) -> None:
    tables = await fx.fetch_many(["GBP", "EUR"], rates_server)
    assert tables["GBP"]["EUR"] == Decimal("1.15")
    assert tables["EUR"]["GBP"] == Decimal("0.87")


@pytest.mark.asyncio
async def test_fetch_many_fails_if_one_base_fails(rates_server: str) -> None:
    with pytest.raises(HTTPError, match="404"):
        await fx.fetch_many(["GBP", "XXX"], rates_server)
