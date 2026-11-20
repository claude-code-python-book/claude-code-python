class OrderRepository(Protocol):
    """What the service needs from order storage."""

    def add(
        self,
        customer_id: str,
        currency: str,
        lines: Sequence[Line],
        created_at: datetime,
    ) -> Order:
        """Store a new order and return it with its id."""
        ...

    def get(self, order_id: int) -> Order | None:
        """Return the order, or None if there is no such id."""
        ...

    def page(
        self, customer_id: str, status: OrderStatus | None, limit: int, offset: int
    ) -> tuple[list[Order], int]:
        """Return one page of a customer's orders, newest first, and the count."""
        ...

    def save(self, order: Order) -> None:
        """Store changes to an existing order."""
        ...
