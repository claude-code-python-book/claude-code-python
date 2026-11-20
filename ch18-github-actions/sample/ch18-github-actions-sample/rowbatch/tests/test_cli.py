from pathlib import Path

import pytest

from rowbatch.cli import main


@pytest.fixture
def orders_csv(tmp_path: Path) -> Path:
    path = tmp_path / "orders.csv"
    lines = ["id,total"] + [f"{n},{n * 10}" for n in range(1, 8)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_cli_reports_batches(
    orders_csv: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(orders_csv), "--size", "3"]) == 0
    assert capsys.readouterr().out == "7 rows in 3 batches of up to 3\n"


def test_cli_exact_fails_on_short_batch(orders_csv: Path) -> None:
    with pytest.raises(ValueError, match="expected 3"):
        main([str(orders_csv), "--size", "3", "--exact"])
