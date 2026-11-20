"""Money helpers: parse amounts into Decimal and round them to cents."""

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def to_money(value: str | int | Decimal) -> Decimal:
    """Convert user input to a Decimal amount, rounded half-up to cents.

    Floats are rejected on purpose: `Decimal(0.1)` is not `Decimal("0.1")`.

    Args:
        value: The amount as a string such as `"19.99"`, an int, or a Decimal.

    Returns:
        The amount quantized to two decimal places, rounding halves up.

    Raises:
        TypeError: If `value` is a float.

    Examples:
        >>> to_money("2.675")
        Decimal('2.68')
        >>> to_money(0.1)
        Traceback (most recent call last):
        ...
        TypeError: pass money as str, int or Decimal, never float
    """
    if isinstance(value, float):
        raise TypeError("pass money as str, int or Decimal, never float")
    return Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)
