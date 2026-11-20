async def customers_with_orders_since(
    session: AsyncSession, since: datetime
) -> Sequence[Customer]:
    """Return customers who ordered since `since`, with only those orders loaded."""
    recent = Order.placed_at >= since
    stmt = (
        select(Customer)
        .where(Customer.orders.any(recent))
        .options(selectinload(Customer.orders.and_(recent)))
        .order_by(Customer.id)
    )
    return (await session.scalars(stmt)).all()
