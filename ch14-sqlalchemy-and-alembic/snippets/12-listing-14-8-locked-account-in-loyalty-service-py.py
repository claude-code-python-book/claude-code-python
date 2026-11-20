async def locked_account(session: AsyncSession, customer_id: int) -> LoyaltyAccount:
    """Return the customer's account, creating it if needed, locked until commit."""
    await session.execute(
        insert(LoyaltyAccount)
        .values(customer_id=customer_id)
        .on_conflict_do_nothing(index_elements=[LoyaltyAccount.customer_id])
    )
    stmt = (
        select(LoyaltyAccount)
        .where(LoyaltyAccount.customer_id == customer_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    return (await session.scalars(stmt)).one()
