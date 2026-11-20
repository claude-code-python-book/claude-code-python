import pandas as pd

from salesreport.clean import clean_orders


def test_regions_are_normalized_and_unknown_ones_kept(raw: pd.DataFrame) -> None:
    regions = clean_orders(raw).orders["region"].tolist()
    assert regions[:4] == ["North", "East", "North", "Central"]


def test_legacy_dates_become_iso(raw: pd.DataFrame) -> None:
    assert clean_orders(raw).orders.loc[1, "order_date"] == "2026-10-02"


def test_thousands_separators_and_status_case(raw: pd.DataFrame) -> None:
    row = clean_orders(raw).orders.loc[1]
    assert (row["unit_price"], row["status"]) == ("1249.00", "completed")


def test_only_exact_duplicates_are_dropped(raw: pd.DataFrame) -> None:
    cleaned = clean_orders(raw)
    assert cleaned.duplicates_dropped == 1
    assert cleaned.orders["order_id"].tolist().count("ORD-000010") == 2


def test_the_input_frame_is_not_changed(raw: pd.DataFrame) -> None:
    before = raw.copy()
    clean_orders(raw)
    pd.testing.assert_frame_equal(raw, before)
