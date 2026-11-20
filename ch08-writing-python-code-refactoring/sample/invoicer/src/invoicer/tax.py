from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


@dataclass(frozen=True)
class Line:
    description: str
    quantity: int
    unit_price: Decimal


def total_with_tax(lines: list[Line], rate: Decimal) -> Decimal:
    """Return the invoice total including tax, rounded to cents."""
    if rate < 0:
        raise ValueError("tax rate cannot be negative")
    net = sum((line.unit_price * line.quantity for line in lines), Decimal("0"))
    gross = net * (1 + rate)
    return gross.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
