"""The loyalty programme's rules, in plain Python.

Nothing here imports SQLAlchemy. The service layer loads data, calls these
functions, and writes the result, so every rule can be tested in
milliseconds without a database.
"""

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import ROUND_FLOOR, Decimal
from enum import StrEnum

CENT = Decimal("0.01")


class Tier(StrEnum):
    """A customer's tier, set by what they spent in the last 12 months."""

    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"


@dataclass(frozen=True)
class Programme:
    """The numbers the business can change without changing the code."""

    silver_from: Decimal = Decimal("500.00")
    gold_from: Decimal = Decimal("2000.00")
    silver_rate: Decimal = Decimal("1.25")
    gold_rate: Decimal = Decimal("1.5")
    point_value: Decimal = Decimal("0.01")  # 100 points = 1.00 off
    min_redeem: int = 500
    max_redeem_share: Decimal = Decimal("0.5")  # at most half an order
    expires_after: timedelta = timedelta(days=365)
    tier_window: timedelta = timedelta(days=365)


PROGRAMME = Programme()


def tier_for(spend_12m: Decimal, programme: Programme = PROGRAMME) -> Tier:
    """Return the tier for a customer's spend over the last 12 months."""
    if spend_12m >= programme.gold_from:
        return Tier.GOLD
    if spend_12m >= programme.silver_from:
        return Tier.SILVER
    return Tier.BRONZE


def points_for_order(
    total: Decimal, tier: Tier, programme: Programme = PROGRAMME
) -> int:
    """Return the points an order earns: one per whole unit, times the tier rate.

    Raises:
        ValueError: If the total is negative.
    """
    if total < 0:
        raise ValueError("An order total can't be negative.")
    rate = {
        Tier.BRONZE: Decimal(1),
        Tier.SILVER: programme.silver_rate,
        Tier.GOLD: programme.gold_rate,
    }[tier]
    return int((total * rate).to_integral_value(rounding=ROUND_FLOOR))


def discount_for(points: int, programme: Programme = PROGRAMME) -> Decimal:
    """Return the money off that a number of points is worth."""
    return (points * programme.point_value).quantize(CENT)


def redemption_problems(
    points: int,
    balance: int,
    order_total: Decimal,
    programme: Programme = PROGRAMME,
) -> list[str]:
    """Return every reason a redemption is refused; an empty list means allowed."""
    problems = []
    if points < programme.min_redeem:
        problems.append(f"Redeem at least {programme.min_redeem} points.")
    if points > balance:
        problems.append(f"The balance is only {balance} points.")
    if discount_for(points, programme) > order_total * programme.max_redeem_share:
        problems.append("Points can pay for at most half of an order.")
    return problems


@dataclass(frozen=True)
class Entry:
    """One line of a customer's points ledger."""

    kind: str  # "earn", "redeem" or "expire"
    points: int  # positive for earn, negative for redeem and expire
    at: datetime


@dataclass
class _Lot:
    points: int
    earned_at: datetime


def points_to_expire(
    entries: list[Entry], as_of: datetime, programme: Programme = PROGRAMME
) -> int:
    """Return how many points have expired by `as_of` and aren't yet written off.

    Points are spent oldest first, so a redemption uses up the points closest
    to expiring. Points expire `expires_after` after they were earned.

    Raises:
        ValueError: If any time is naive.
    """
    if as_of.tzinfo is None or any(e.at.tzinfo is None for e in entries):
        raise ValueError("Use timezone-aware datetimes.")
    lots: deque[_Lot] = deque()
    expired = 0

    def expire_until(moment: datetime) -> None:
        nonlocal expired
        while lots and lots[0].earned_at + programme.expires_after <= moment:
            expired += lots.popleft().points

    def spend(points: int) -> None:
        while points and lots:
            used = min(points, lots[0].points)
            lots[0].points -= used
            points -= used
            if lots[0].points == 0:
                lots.popleft()

    for entry in sorted(entries, key=lambda e: e.at):
        expire_until(entry.at)
        if entry.kind == "earn":
            lots.append(_Lot(entry.points, entry.at))
        elif entry.kind == "expire":
            expired += entry.points  # negative: already written off
        else:
            spend(-entry.points)
    expire_until(as_of)
    return max(expired, 0)
