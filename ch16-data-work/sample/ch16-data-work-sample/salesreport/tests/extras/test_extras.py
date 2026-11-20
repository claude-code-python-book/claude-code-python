"""Checks for the optional Polars, Pandera and Plotly code.

Each test is skipped when its library isn't installed (as it wasn't where
the book was written, so these three were never run there).
"""

from pathlib import Path

import pandas as pd
import pytest

from salesreport.clean import clean_orders
from salesreport.report import summarize
from salesreport.validate import split_valid


@pytest.fixture
def valid(raw: pd.DataFrame) -> pd.DataFrame:
    return split_valid(clean_orders(raw).orders, month="2026-10").valid


def test_polars_matches_pandas(valid: pd.DataFrame, tmp_path: Path) -> None:
    pytest.importorskip("polars")
    from extras.report_polars import revenue_by_region

    path = tmp_path / "orders-valid.csv"
    valid.to_csv(path, index=False)
    expected = summarize(valid, "2026-10").by_region
    assert revenue_by_region(str(path)).rows() == list(
        expected.itertuples(index=False, name=None)
    )


def test_pandera_accepts_valid_and_rejects_bad(valid: pd.DataFrame) -> None:
    pa = pytest.importorskip("pandera.pandas")
    from extras.schema_pandera import ValidOrders

    ValidOrders.validate(valid)
    with pytest.raises(pa.errors.SchemaError):
        ValidOrders.validate(valid.assign(quantity=0))


def test_plotly_writes_html(valid: pd.DataFrame, tmp_path: Path) -> None:
    pytest.importorskip("plotly")
    from extras.chart_plotly import daily_revenue_html

    path = tmp_path / "daily.html"
    daily_revenue_html(summarize(valid, "2026-10").daily, path)
    assert "<div" in path.read_text()
