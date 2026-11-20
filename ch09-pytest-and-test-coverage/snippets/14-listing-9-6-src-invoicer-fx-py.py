"""Convert billed amounts between currencies with published exchange rates."""

import asyncio
import json
from collections.abc import Iterable
from decimal import ROUND_HALF_UP, Decimal
from urllib.request import urlopen

CENT = Decimal("0.01")
RATES_URL = "https://rates.example.com/latest"


def fetch_rates(base: str, url: str = RATES_URL) -> dict[str, Decimal]:
    """Return the rates from `base` to other currencies, as published at `url`."""
    with urlopen(f"{url}?base={base}", timeout=5) as response:
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
