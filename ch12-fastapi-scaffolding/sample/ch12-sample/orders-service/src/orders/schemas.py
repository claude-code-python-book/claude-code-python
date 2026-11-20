"""Request and response models: the shapes the API accepts and returns."""

from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator

from orders.domain import OrderStatus

Sku = Annotated[str, Field(pattern=r"^[A-Z0-9-]{3,20}$", examples=["MUG-01"])]
Money = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]


class LineIn(BaseModel):
    """One line of a new order."""

    model_config = ConfigDict(extra="forbid")

    sku: Sku
    quantity: int = Field(gt=0, le=100)
    unit_price: Money


class OrderCreate(BaseModel):
    """The body of POST /orders. The customer comes from the access token."""

    model_config = ConfigDict(extra="forbid")

    currency: Literal["GBP", "EUR", "USD"]
    lines: list[LineIn] = Field(min_length=1, max_length=50)

    @model_validator(mode="after")
    def skus_are_unique(self) -> Self:
        """Reject an order that lists the same SKU twice."""
        skus = [line.sku for line in self.lines]
        if len(skus) != len(set(skus)):
            raise ValueError("each SKU may appear once; add up the quantities")
        return self


class LineOut(BaseModel):
    """One line of an order in a response."""

    model_config = ConfigDict(from_attributes=True)

    sku: str
    quantity: int
    unit_price: Decimal


class OrderRead(BaseModel):
    """An order as the API returns it."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: str
    currency: str
    status: OrderStatus
    lines: list[LineOut]
    created_at: datetime

    @computed_field  # type: ignore[prop-decorator]
    @property
    def total(self) -> Decimal:
        """The sum of quantity times unit price over all lines."""
        return sum((x.unit_price * x.quantity for x in self.lines), Decimal("0.00"))


class Page[T](BaseModel):
    """One page of a list, with the total count for paging."""

    items: list[T]
    count: int
    limit: int
    offset: int


class Token(BaseModel):
    """The response of POST /auth/token, as OAuth2 defines it."""

    access_token: str
    token_type: str


class Problem(BaseModel):
    """An error response in the RFC 9457 problem details format."""

    type: str = "about:blank"
    title: str
    status: int
    detail: str
    instance: str
