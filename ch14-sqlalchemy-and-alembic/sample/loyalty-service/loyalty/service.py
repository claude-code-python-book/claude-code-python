"""The loyalty feature: rules from rules.py, applied inside a transaction.

Every function takes an AsyncSession that is already in a transaction and
leaves committing to the caller:

    async with Session.begin() as session:
        await record_order(session, customer_id, total, placed_at)
"""

from collections.abc import Sequence
from datetime import datetime
from decimal import Decimal
from typing import NamedTuple

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from loyalty import rules
from loyalty.models import Customer, LoyaltyAccount, Order, PointsEntry


class RedemptionRefusedError(Exception):
    """Raised when a redemption breaks a rule; `problems` says which."""

    def __init__(self, problems: list[str]) -> None:
        super().__init__("; ".join(problems))
        self.problems = problems


class TopCustomer(NamedTuple):
    """One row of the top-customers report."""

    id: int
    name: str
    spend: Decimal


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


async def record_order(
    session: AsyncSession, customer_id: int, total: Decimal, placed_at: datetime
) -> int:
    """Store an order and award its points; return the points earned."""
    order = Order(customer_id=customer_id, total=total, placed_at=placed_at)
    session.add(order)
    await session.flush()  # assigns order.id
    account = await locked_account(session, customer_id)
    points = rules.points_for_order(total, rules.Tier(account.tier))
    if points:
        session.add(
            PointsEntry(
                customer_id=customer_id, kind="earn", points=points, order_id=order.id
            )
        )
        account.balance += points
    return points


async def redeem(
    session: AsyncSession, customer_id: int, points: int, order_total: Decimal
) -> Decimal:
    """Spend points against an order; return the discount.

    Raises:
        RedemptionRefusedError: If the redemption breaks a rule.
    """
    account = await locked_account(session, customer_id)
    problems = rules.redemption_problems(points, account.balance, order_total)
    if problems:
        raise RedemptionRefusedError(problems)
    session.add(PointsEntry(customer_id=customer_id, kind="redeem", points=-points))
    account.balance -= points
    return rules.discount_for(points)


async def spend_in_window(
    session: AsyncSession, customer_id: int, now: datetime
) -> Decimal:
    """Return what the customer spent in the tier window before `now`."""
    stmt = select(func.coalesce(func.sum(Order.total), 0)).where(
        Order.customer_id == customer_id,
        Order.placed_at > now - rules.PROGRAMME.tier_window,
    )
    return Decimal(await session.scalar(stmt) or 0)


async def refresh_tier(session: AsyncSession, customer_id: int, now: datetime) -> str:
    """Recalculate the customer's tier from their recent spend."""
    account = await locked_account(session, customer_id)
    account.tier = rules.tier_for(await spend_in_window(session, customer_id, now))
    return account.tier


async def expire_points(session: AsyncSession, customer_id: int, now: datetime) -> int:
    """Write off points that have expired; return how many."""
    account = await locked_account(session, customer_id)
    rows = await session.scalars(
        select(PointsEntry)
        .where(PointsEntry.customer_id == customer_id)
        .order_by(PointsEntry.created_at, PointsEntry.id)
    )
    entries = [rules.Entry(e.kind, e.points, e.created_at) for e in rows]
    points = rules.points_to_expire(entries, now)
    if points:
        session.add(
            PointsEntry(
                customer_id=customer_id, kind="expire", points=-points, created_at=now
            )
        )
        account.balance -= points
    return points


async def top_customers(
    session: AsyncSession, since: datetime, limit: int = 10
) -> list[TopCustomer]:
    """Return the biggest spenders since `since`, in one query."""
    spend = func.sum(Order.total).label("spend")
    stmt = (
        select(Customer.id, Customer.name, spend)
        .join(Customer.orders)
        .where(Order.placed_at >= since)
        .group_by(Customer.id)
        .order_by(spend.desc(), Customer.id)
        .limit(limit)
    )
    return [TopCustomer(*row) for row in await session.execute(stmt)]


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
