from decimal import Decimal

from invoicer.billing import late_fee


def test_late_fee_first_period_is_one_and_a_half_percent() -> None:
    assert late_fee(Decimal("100.00"), 31) == Decimal("1.50")


def test_late_fee_adds_a_period_every_thirty_days() -> None:
    assert late_fee(Decimal("100.00"), 61) == Decimal("3.00")


def test_late_fee_is_capped_at_ten_percent_of_gross() -> None:
    assert late_fee(Decimal("100.00"), 3650) == Decimal("10.00")


def test_late_fee_rounds_half_up_to_the_cent() -> None:
    # 3.00 * 1.5% = 0.045: half-up gives 0.05, banker's rounding 0.04
    assert late_fee(Decimal("3.00"), 31) == Decimal("0.05")
