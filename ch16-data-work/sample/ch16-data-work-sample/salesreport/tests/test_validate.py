import pandas as pd
import pytest

from salesreport.clean import clean_orders
from salesreport.validate import check_frame, split_valid


@pytest.fixture
def checked(raw: pd.DataFrame):
    return split_valid(clean_orders(raw).orders, month="2026-10")


def test_valid_rows_are_typed(checked) -> None:
    valid = checked.valid
    assert valid["order_id"].tolist() == [
        "ORD-000001",
        "ORD-000002",
        "ORD-000003",
        "ORD-000008",
        "ORD-000009",
    ]
    assert str(valid["order_date"].dtype).startswith("datetime64")
    assert valid.loc[1, "unit_price_cents"] == 124900


def test_each_reject_says_why(checked) -> None:
    reasons = dict(
        zip(checked.rejected["order_id"], checked.rejected["reason"], strict=True)
    )
    assert reasons["ORD-000004"].startswith("region: Input should be")
    assert reasons["ORD-000005"] == "quantity: Input should be greater than 0"
    assert reasons["ORD-000006"] == "unit_price: Input should be a valid decimal"
    assert reasons["ORD-000007"] == ("order_date: Value error, date is outside 2026-10")
    assert reasons["ORD-000010"].startswith("order_id: appears twice")


def test_nothing_is_lost(raw: pd.DataFrame, checked) -> None:
    assert len(checked.valid) + len(checked.rejected) + 1 == len(raw)


def test_check_frame_catches_a_duplicate_id(checked) -> None:
    doubled = pd.concat([checked.valid, checked.valid.head(1)])
    with pytest.raises(ValueError, match="not unique"):
        check_frame(doubled)
