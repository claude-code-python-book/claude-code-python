from pathlib import Path

import matplotlib.pyplot as plt
import pytest

from salesreport.pipeline import run

ROOT = Path(__file__).parents[1]
SAMPLE = ROOT / "data/sample/orders-sample.csv"
GOLDEN = Path(__file__).parent / "golden/report-sample.md"


def test_sample_report_matches_golden_file(tmp_path: Path) -> None:
    result = run(SAMPLE, tmp_path, "2026-10")
    assert (tmp_path / "report.md").read_text() == GOLDEN.read_text()
    assert (
        result.rows_read == result.valid + result.rejected + result.duplicates_dropped
    )


def test_chart_is_written(tmp_path: Path) -> None:
    run(SAMPLE, tmp_path, "2026-10")
    height, width, _ = plt.imread(tmp_path / "daily_revenue.png").shape
    assert (width, height) == (1600, 720)


def test_refuses_to_write_into_raw_data(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="raw data"):
        run(SAMPLE, tmp_path / "raw", "2026-10")
