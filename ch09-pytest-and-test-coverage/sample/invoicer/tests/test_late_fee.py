from decimal import Decimal

import pytest

from invoicer.billing import late_fee


@pytest.mark.parametrize(
    ("days", "expected"),
    [
        pytest.param(31, "1.50", id="first-overdue-day"),
        pytest.param(59, "1.50", id="last-day-of-first-period"),
        pytest.param(
            60,
            "1.50",
            id="day-60",
            marks=pytest.mark.xfail(
                strict=True, reason="docstring says one period at day 60; code: two"
            ),
        ),
        pytest.param(61, "3.00", id="second-period"),
        pytest.param(209, "9.00", id="six-periods-below-cap"),
        pytest.param(210, "10.00", id="seventh-period-hits-cap"),
        pytest.param(3650, "10.00", id="capped"),
    ],
)
def test_late_fee_on_a_100_invoice(days: int, expected: str) -> None:
    assert late_fee(Decimal("100.00"), days) == Decimal(expected)


def test_late_fee_rounds_half_up_to_the_cent() -> None:
    # 3.00 * 1.5% = 0.045: half-up gives 0.05, banker's rounding 0.04
    assert late_fee(Decimal("3.00"), 31) == Decimal("0.05")
