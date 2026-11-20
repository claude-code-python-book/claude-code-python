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
