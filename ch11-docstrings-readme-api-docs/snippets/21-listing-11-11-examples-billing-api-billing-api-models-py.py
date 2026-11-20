"""Response models for the billing API."""

from decimal import Decimal

from pydantic import BaseModel, Field


class Converted(BaseModel):
    """An amount converted to another currency."""

    amount: Decimal = Field(
        description="The converted amount, rounded half-up to cents.",
        examples=["11.85"],
    )
    currency: str = Field(
        description="ISO 4217 code of the currency `amount` is in.",
        examples=["EUR"],
        min_length=3,
        max_length=3,
    )
