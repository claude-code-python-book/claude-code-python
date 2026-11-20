from decimal import Decimal

import pytest

from invoicer import to_money


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("2.675", "2.68"), ("0.125", "0.13"), (3, "3.00"), (Decimal("1.005"), "1.01")],
)
def test_to_money_rounds_half_up(raw: str | int | Decimal, expected: str) -> None:
    assert to_money(raw) == Decimal(expected)


def test_to_money_rejects_float() -> None:
    with pytest.raises(TypeError, match="never float"):
        to_money(0.1)  # type: ignore[arg-type]
