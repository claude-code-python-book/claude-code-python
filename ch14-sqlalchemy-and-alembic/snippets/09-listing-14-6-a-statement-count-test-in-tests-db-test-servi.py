async def test_listing_customers_costs_two_queries_however_many_there_are(
    session: AsyncSession, count_statements: StatementCounter
) -> None:
    for n in range(1, 21):
        customer = await new_customer(session, n)
        await service.record_order(session, customer.id, Decimal("10.00"), NOW)
    since = NOW - timedelta(days=30)
    await session.flush()  # so autoflush has nothing to send
    count_statements.statements.clear()

    customers = await service.customers_with_orders_since(session, since)
    totals = [sum(o.total for o in c.orders) for c in customers]

    assert len(customers) == 20 and set(totals) == {Decimal("10.00")}
    assert len(count_statements.statements) == 2  # customers, then all orders
