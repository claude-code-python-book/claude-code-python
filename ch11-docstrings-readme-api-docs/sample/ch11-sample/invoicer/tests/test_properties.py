from decimal import ROUND_HALF_UP, Decimal

from hypothesis import example, given
from hypothesis import strategies as st

from invoicer import to_money
from invoicer.billing import CENT, late_fee

amounts = st.decimals(min_value=0, max_value=1_000_000, places=2)
overdue_days = st.integers(min_value=31, max_value=36_500)


@given(st.decimals(min_value=-(10**9), max_value=10**9))
def test_to_money_rounds_to_the_nearest_cent(value: Decimal) -> None:
    money = to_money(value)
    assert money.as_tuple().exponent == -2
    assert abs(money - value) <= Decimal("0.005")
    assert to_money(money) == money


@given(gross=amounts, days=overdue_days)
@example(gross=Decimal("0.00"), days=31)
def test_late_fee_stays_between_zero_and_the_cap(gross: Decimal, days: int) -> None:
    cap = (gross * Decimal("0.10")).quantize(CENT, rounding=ROUND_HALF_UP)
    assert Decimal("0.00") <= late_fee(gross, days) <= cap


@given(gross=amounts, days=overdue_days)
def test_late_fee_never_drops_as_days_pass(gross: Decimal, days: int) -> None:
    assert late_fee(gross, days + 1) >= late_fee(gross, days)
