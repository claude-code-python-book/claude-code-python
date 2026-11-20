"""A small HTTP API in front of invoicer's currency conversion."""

from collections.abc import Callable
from decimal import ROUND_HALF_UP, Decimal
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from invoicer import fx
from pydantic import BaseModel

RateFetcher = Callable[[str], dict[str, Decimal]]

app = FastAPI()


def get_fetch_rates() -> RateFetcher:
    return fx.fetch_rates


class Converted(BaseModel):
    amount: Decimal
    currency: str


@app.get("/convert")
def convert(
    amount: Decimal,
    base: str,
    target: str,
    fetch_rates: Annotated[RateFetcher, Depends(get_fetch_rates)],
) -> Converted:
    rates = fetch_rates(base)
    if target not in rates:
        raise HTTPException(404, detail=f"no rate from {base} to {target}")
    converted = (amount * rates[target]).quantize(fx.CENT, rounding=ROUND_HALF_UP)
    return Converted(amount=converted, currency=target)
