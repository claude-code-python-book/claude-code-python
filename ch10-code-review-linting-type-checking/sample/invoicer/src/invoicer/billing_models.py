"""Typed records for the billing run.

`BillingRow` validates raw CSV values at the boundary. The dataclasses
carry trusted values between the steps of the run.
"""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Region = Literal["UK", "DE", "US-CA", "IN"]
Discount = Literal["", "SAVE10", "BULK5"]
Status = Literal["paid", "open", "overdue"]


class BillingRow(BaseModel):
    """One row of a billing export, validated."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    invoice_id: str = Field(min_length=1)
    customer: str = Field(min_length=1)
    region: Region
    sku: str = Field(min_length=1)
    qty: int = Field(gt=0)
    unit_price: Decimal = Field(ge=0, allow_inf_nan=False)
    discount: Discount = ""
    issued: date
    paid: date | None = None

    @field_validator("qty", mode="before")
    @classmethod
    def whole_number(cls, value: object) -> object:
        """Parse quantities as the old code did, with int(), so "4.0" fails."""
        if not isinstance(value, str):
            return value
        try:
            return int(value)
        except ValueError:
            raise ValueError("must be a whole number") from None

    @field_validator("issued", "paid", mode="before")
    @classmethod
    def calendar_day(cls, value: object) -> object:
        """Accept YYYY-MM-DD as the old code did; a blank value means None."""
        if not isinstance(value, str):
            return value
        if not value.strip():
            return None
        try:
            return datetime.strptime(value.strip(), "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("must be a date in YYYY-MM-DD form") from None

    @model_validator(mode="after")
    def paid_after_issued(self) -> Self:
        if self.paid is not None and self.paid < self.issued:
            raise ValueError("paid before issued")
        return self


@dataclass
class Invoice:
    """An invoice being assembled from its rows."""

    invoice_id: str
    customer: str
    region: Region
    issued: date
    paid: date | None
    net: Decimal
    lines: int = 1


@dataclass(frozen=True)
class Bill:
    """The billed result for one invoice."""

    customer: str
    lines: int
    gross: Decimal
    fee: Decimal
    status: Status

    def to_dict(self) -> dict[str, str | int]:
        return {
            "customer": self.customer,
            "lines": self.lines,
            "gross": str(self.gross),
            "fee": str(self.fee),
            "status": self.status,
        }


@dataclass
class CustomerTotals:
    """Running totals for one customer."""

    invoices: int = 0
    billed: Decimal = Decimal("0")
    fees: Decimal = Decimal("0")
    outstanding: Decimal = Decimal("0")

    def add(self, bill: Bill) -> None:
        self.invoices += 1
        self.billed += bill.gross
        self.fees += bill.fee
        if bill.status != "paid":
            self.outstanding += bill.gross + bill.fee

    def to_dict(self) -> dict[str, str | int]:
        return {
            "invoices": self.invoices,
            "billed": str(self.billed),
            "fees": str(self.fees),
            "outstanding": str(self.outstanding),
        }
