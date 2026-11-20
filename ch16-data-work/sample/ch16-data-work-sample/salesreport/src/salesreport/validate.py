"""Parse each cleaned row with Pydantic and split valid rows from rejects."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Annotated, Literal

import pandas as pd
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    ValidationError,
    ValidationInfo,
    field_validator,
)

OrderId = Annotated[str, StringConstraints(pattern=r"^ORD-\d{6}$")]
Price = Annotated[Decimal, Field(gt=0, max_digits=9, decimal_places=2)]


class Order(BaseModel):
    """One valid order line. Strings from the CSV are parsed into types."""

    model_config = ConfigDict(frozen=True)

    order_id: OrderId
    order_date: date
    region: Literal["North", "South", "East", "West"]
    product: Annotated[str, StringConstraints(min_length=1)]
    quantity: Annotated[int, Field(gt=0)]
    unit_price: Price
    status: Literal["completed", "cancelled", "refunded"]

    @field_validator("order_date")
    @classmethod
    def in_report_month(cls, value: date, info: ValidationInfo) -> date:
        """Reject dates outside the month passed in the validation context."""
        month = (info.context or {}).get("month")
        if month and value.strftime("%Y-%m") != month:
            raise ValueError(f"date is outside {month}")
        return value


@dataclass(frozen=True)
class Checked:
    """Typed valid orders and the rejected rows with a reason for each."""

    valid: pd.DataFrame
    rejected: pd.DataFrame


def _reason(error: ValidationError) -> str:
    return "; ".join(
        f"{'.'.join(map(str, e['loc']))}: {e['msg']}"
        for e in error.errors(include_url=False)
    )


def split_valid(cleaned: pd.DataFrame, month: str) -> Checked:
    """Validate every row; conflicting duplicate order IDs are all rejected."""
    clash = cleaned["order_id"].duplicated(keep=False)
    good: list[Order] = []
    bad: list[dict[str, str]] = []
    for position, row in enumerate(cleaned.to_dict("records")):
        if clash.iloc[position]:
            bad.append(
                {**row, "reason": "order_id: appears twice with different values"}
            )
            continue
        try:
            good.append(Order.model_validate(row, context={"month": month}))
        except ValidationError as error:
            bad.append({**row, "reason": _reason(error)})
    return Checked(
        _to_frame(good), pd.DataFrame(bad, columns=[*cleaned.columns, "reason"])
    )


def _to_frame(orders: list[Order]) -> pd.DataFrame:
    frame = pd.DataFrame(
        {
            "order_id": pd.Series([o.order_id for o in orders], dtype="str"),
            "order_date": pd.to_datetime(
                pd.Series([o.order_date for o in orders], dtype="object")
            ),
            "region": pd.Series([o.region for o in orders], dtype="str"),
            "product": pd.Series([o.product for o in orders], dtype="str"),
            "quantity": pd.Series([o.quantity for o in orders], dtype="int64"),
            "unit_price_cents": pd.Series(
                [int(o.unit_price * 100) for o in orders], dtype="int64"
            ),
            "status": pd.Series([o.status for o in orders], dtype="str"),
        }
    )
    check_frame(frame)
    return frame


def check_frame(valid: pd.DataFrame) -> None:
    """Check what no single row can see: uniqueness and column types."""
    if not valid["order_id"].is_unique:
        raise ValueError("order_id is not unique")
    expected = {"quantity": "int64", "unit_price_cents": "int64"}
    for column, dtype in expected.items():
        if str(valid[column].dtype) != dtype:
            raise TypeError(f"{column} is {valid[column].dtype}, not {dtype}")
