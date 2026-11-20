from pathlib import Path

import pytest

from salesreport.load import read_orders


def test_every_column_is_text_and_blanks_stay_blank(tmp_path: Path) -> None:
    path = tmp_path / "export.csv"
    path.write_text(
        "order_id,order_date,region,product,quantity,unit_price,status\n"
        'ORD-000001,2026-10-01,,Mouse,2,"1,249.00",completed\n'
    )
    frame = read_orders(path)
    assert {str(t) for t in frame.dtypes} == {"str"}
    assert frame.loc[0, "region"] == ""
    assert frame.loc[0, "unit_price"] == "1,249.00"


def test_a_missing_column_is_named(tmp_path: Path) -> None:
    path = tmp_path / "export.csv"
    path.write_text("order_id,order_date\nORD-000001,2026-10-01\n")
    with pytest.raises(ValueError, match="missing columns"):
        read_orders(path)
