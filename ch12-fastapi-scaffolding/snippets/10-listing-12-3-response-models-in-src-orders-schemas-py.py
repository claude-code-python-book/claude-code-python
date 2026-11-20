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
