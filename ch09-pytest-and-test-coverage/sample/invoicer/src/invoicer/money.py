from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def to_money(value: str | int | Decimal) -> Decimal:
    """Convert user input to a Decimal amount, rounded half-up to cents.

    Floats are rejected on purpose: Decimal(0.1) is not Decimal("0.1").
    """
    if isinstance(value, float):
        raise TypeError("pass money as str, int or Decimal, never float")
    return Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)
