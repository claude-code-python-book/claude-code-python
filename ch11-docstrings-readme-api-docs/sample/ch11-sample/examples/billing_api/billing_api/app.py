"""A small HTTP API in front of invoicer's currency conversion."""

from collections.abc import Callable
from decimal import ROUND_HALF_UP, Decimal
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from invoicer import fx

from billing_api.models import Converted

RateFetcher = Callable[[str], dict[str, Decimal]]

app = FastAPI(
    title="Billing API",
    summary="Currency conversion for invoices.",
    description="Converts invoice amounts with the rates the finance team publishes.",
    version="1.2.0",
    openapi_tags=[{"name": "fx", "description": "Exchange rates and conversion."}],
)


def get_fetch_rates() -> RateFetcher:
    """Return the function that fetches rates; tests override this dependency."""
    return fx.fetch_rates


@app.get(
    "/convert",
    tags=["fx"],
    summary="Convert an amount",
    response_description="The converted amount and its currency",
    responses={404: {"description": "No rate between the two currencies"}},
)
def convert(
    amount: Annotated[Decimal, Query(description="Amount in the base currency.")],
    base: Annotated[str, Query(description="ISO 4217 code, such as GBP.")],
    target: Annotated[str, Query(description="ISO 4217 code to convert to.")],
    fetch_rates: Annotated[RateFetcher, Depends(get_fetch_rates)],
) -> Converted:
    """Convert `amount` from `base` to `target` at today's published rate.

    The result is rounded **half-up** to cents, the rule used on invoices.
    \f
    The text after the form feed above is for Python readers only: FastAPI
    leaves it out of the OpenAPI description. The form feed must be a real
    character, so this docstring can't be a raw string.
    """  # noqa: D301
    rates = fetch_rates(base)
    if target not in rates:
        raise HTTPException(404, detail=f"no rate from {base} to {target}")
    converted = (amount * rates[target]).quantize(fx.CENT, rounding=ROUND_HALF_UP)
    return Converted(amount=converted, currency=target)
