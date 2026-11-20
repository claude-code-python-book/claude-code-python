from pathlib import Path

import pytest

from invoicer.cli import main

SAMPLE = Path(__file__).parent / "data" / "billing_sample.csv"
HEADER = "invoice_id,customer,region,sku,qty,unit_price,issued\n"


def test_prints_totals_and_reports_rejected_rows(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main([str(SAMPLE), "--today", "2026-11-15"]) == 1
    out, err = capsys.readouterr()
    assert "Acme Ltd: billed 188.18, outstanding 142.50" in out
    assert out.endswith("Grand total: 2012.00\n")
    assert err.startswith("row 12: sku:")


def test_clean_export_exits_zero(tmp_path: Path) -> None:
    export = tmp_path / "export.csv"
    export.write_text(HEADER + "INV-1,Acme Ltd,UK,WIDGET,3,9.99,2026-11-01\n")
    assert main([str(export), "--today", "2026-11-15"]) == 0


def test_writes_the_customer_report(tmp_path: Path) -> None:
    main([str(SAMPLE), "--today", "2026-11-15", "--report-dir", str(tmp_path)])
    assert (tmp_path / "customers.csv").read_text().startswith("customer,invoices")


def test_missing_columns_are_a_usage_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    export = tmp_path / "export.csv"
    export.write_text("invoice_id,customer\nINV-1,Acme Ltd\n")
    with pytest.raises(SystemExit) as exit_info:
        main([str(export)])
    assert exit_info.value.code == 2
    assert (
        "missing columns: issued, qty, region, sku, unit_price"
        in capsys.readouterr().err
    )
