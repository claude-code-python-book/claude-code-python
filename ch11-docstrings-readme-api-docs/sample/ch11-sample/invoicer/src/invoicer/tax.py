"""Invoice lines and totals with tax."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


@dataclass(frozen=True)
class Line:
    """One line of an invoice: what was sold, how many, and at what price."""

    description: str
    quantity: int
    unit_price: Decimal


def total_with_tax(lines: list[Line], rate: Decimal) -> Decimal:
    """Return the invoice total including tax, rounded to cents.

    Args:
        lines: The invoice lines. An empty list gives a total of `0.00`.
        rate: The tax rate as a fraction, such as `Decimal("0.20")` for 20%.

    Returns:
        The sum of quantity times unit price over all lines, plus tax, rounded
        half-up to cents once, at the end.

    Raises:
        ValueError: If `rate` is negative.
    """
    if rate < 0:
        raise ValueError("tax rate cannot be negative")
    net = sum((line.unit_price * line.quantity for line in lines), Decimal("0"))
    gross = net * (1 + rate)
    return gross.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
