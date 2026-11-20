from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession

from loyalty import service
from loyalty.models import Customer, LoyaltyAccount, Order, PointsEntry

from .conftest import StatementCounter

NOW = datetime(2026, 11, 16, 12, 0, tzinfo=UTC)


async def new_customer(session: AsyncSession, n: int = 1) -> Customer:
    customer = Customer(email=f"c{n}@example.com", name=f"Customer {n}")
    session.add(customer)
    await session.flush()
    return customer


async def test_an_order_earns_points_and_updates_the_balance(
    session: AsyncSession,
) -> None:
    customer = await new_customer(session)
    points = await service.record_order(session, customer.id, Decimal("120.50"), NOW)
    account = await session.get(LoyaltyAccount, customer.id)
    assert points == 120
    assert account is not None and account.balance == 120


async def test_an_order_cannot_earn_twice(session: AsyncSession) -> None:
    customer = await new_customer(session)
    await service.record_order(session, customer.id, Decimal("50.00"), NOW)
    order_id = await session.scalar(select(Order.id))
    session.add(
        PointsEntry(customer_id=customer.id, kind="earn", points=50, order_id=order_id)
    )
    with pytest.raises(IntegrityError, match="uq_points_entries_earn_order"):
        await session.flush()


async def test_the_database_refuses_a_negative_balance(session: AsyncSession) -> None:
    customer = await new_customer(session)
    account = await service.locked_account(session, customer.id)
    account.balance = -1
    with pytest.raises(IntegrityError, match="balance_not_negative"):
        await session.flush()


async def test_a_refused_redemption_changes_nothing(session: AsyncSession) -> None:
    customer = await new_customer(session)
    await service.record_order(session, customer.id, Decimal("300.00"), NOW)
    with pytest.raises(service.RedemptionRefusedError) as refused:
        await service.redeem(session, customer.id, 600, Decimal("100.00"))
    assert refused.value.problems == ["The balance is only 300 points."]
    assert (await service.locked_account(session, customer.id)).balance == 300


async def test_tiers_follow_the_last_twelve_months(session: AsyncSession) -> None:
    customer = await new_customer(session)
    old = NOW - timedelta(days=400)
    await service.record_order(session, customer.id, Decimal("1800.00"), old)
    await service.record_order(session, customer.id, Decimal("600.00"), NOW)
    assert await service.refresh_tier(session, customer.id, NOW) == "silver"


async def test_expired_points_are_written_off_once(session: AsyncSession) -> None:
    customer = await new_customer(session)
    earned = NOW - timedelta(days=366)
    await service.record_order(session, customer.id, Decimal("80.00"), earned)
    entry = await session.scalar(select(PointsEntry))
    assert entry is not None
    entry.created_at = earned  # the ledger line is as old as the order
    assert await service.expire_points(session, customer.id, NOW) == 80
    assert await service.expire_points(session, customer.id, NOW) == 0


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


async def test_lazy_loading_is_an_error_not_a_query(session: AsyncSession) -> None:
    customer = await new_customer(session)
    session.expunge(customer)
    loaded = await session.scalar(select(Customer).where(Customer.id == customer.id))
    assert loaded is not None
    with pytest.raises(InvalidRequestError, match="lazy='raise'"):
        _ = loaded.orders
