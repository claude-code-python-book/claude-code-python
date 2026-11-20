"""Convert billed amounts between currencies with published exchange rates."""

import asyncio
import json
from collections.abc import Iterable
from decimal import ROUND_HALF_UP, Decimal
from urllib.parse import urlsplit
from urllib.request import urlopen

CENT = Decimal("0.01")
RATES_URL = "https://rates.example.com/latest"


def fetch_rates(base: str, url: str = RATES_URL) -> dict[str, Decimal]:
    """Return the rates from `base` to other currencies, as published at `url`."""
    if urlsplit(url).scheme not in ("http", "https"):
        raise ValueError(f"rates URL must use http or https, not {url!r}")
    # The scheme is checked above, so urlopen can't be pointed at file: URLs.
    with urlopen(f"{url}?base={base}", timeout=5) as response:  # noqa: S310
        data = json.load(response, parse_float=Decimal)
    return {code: Decimal(rate) for code, rate in data["rates"].items()}


def convert(amount: Decimal, base: str, target: str, url: str = RATES_URL) -> Decimal:
    """Convert `amount` from `base` to `target`, rounded half-up to cents."""
    if base == target:
        return amount
    rates = fetch_rates(base, url)
    if target not in rates:
        raise ValueError(f"no rate from {base} to {target}")
    return (amount * rates[target]).quantize(CENT, rounding=ROUND_HALF_UP)


async def fetch_many(
    bases: Iterable[str], url: str = RATES_URL
) -> dict[str, dict[str, Decimal]]:
    """Fetch the rates for several base currencies concurrently."""
    codes = list(bases)
    tables = await asyncio.gather(
        *(asyncio.to_thread(fetch_rates, code, url) for code in codes)
    )
    return dict(zip(codes, tables, strict=True))
