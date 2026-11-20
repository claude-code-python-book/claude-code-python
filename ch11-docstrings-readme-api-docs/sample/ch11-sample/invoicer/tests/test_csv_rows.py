from pathlib import Path

import pytest

from invoicer.csv_rows import read_rows


def write(tmp_path: Path, text: str, encoding: str = "utf-8") -> Path:
    path = tmp_path / "export.csv"
    path.write_text(text, encoding=encoding)
    return path


def test_reads_rows_keyed_by_header(tmp_path: Path) -> None:
    path = write(tmp_path, "sku,qty\nWIDGET,3\nCABLE,2\n")
    assert read_rows(path) == [
        {"sku": "WIDGET", "qty": "3"},
        {"sku": "CABLE", "qty": "2"},
    ]


def test_accepts_excel_byte_order_mark(tmp_path: Path) -> None:
    path = write(tmp_path, "sku,qty\nWIDGET,3\n", encoding="utf-8-sig")
    assert read_rows(path, required=["sku"]) == [{"sku": "WIDGET", "qty": "3"}]


def test_strips_whitespace_and_fills_short_rows(tmp_path: Path) -> None:
    path = write(tmp_path, " sku , qty ,paid\n WIDGET , 3\n")
    assert read_rows(path) == [{"sku": "WIDGET", "qty": "3", "paid": ""}]


def test_skips_blank_rows(tmp_path: Path) -> None:
    path = write(tmp_path, "sku,qty\n\n,\nWIDGET,3\n , \n")
    assert read_rows(path) == [{"sku": "WIDGET", "qty": "3"}]


def test_lists_every_missing_column(tmp_path: Path) -> None:
    path = write(tmp_path, "sku\nWIDGET\n")
    with pytest.raises(ValueError, match="missing columns: qty, unit_price"):
        read_rows(path, required=["unit_price", "sku", "qty"])


def test_rejects_rows_with_too_many_values(tmp_path: Path) -> None:
    path = write(tmp_path, "sku,qty\nWIDGET,3\nCABLE,2,extra\n")
    with pytest.raises(ValueError, match="row 3 has too many values"):
        read_rows(path)


def test_empty_file_has_no_rows(tmp_path: Path) -> None:
    assert read_rows(write(tmp_path, "")) == []


def test_detects_semicolon_delimiter(tmp_path: Path) -> None:
    path = write(tmp_path, "sku;description\nWIDGET;Blue, large\n")
    assert read_rows(path) == [{"sku": "WIDGET", "description": "Blue, large"}]
