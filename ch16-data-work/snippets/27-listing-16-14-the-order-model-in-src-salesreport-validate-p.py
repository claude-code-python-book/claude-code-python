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
