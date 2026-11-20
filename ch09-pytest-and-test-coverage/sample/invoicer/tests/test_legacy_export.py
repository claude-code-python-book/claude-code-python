from decimal import Decimal

from invoicer import Line
from invoicer.legacy_export import export_csv_row


def test_export_csv_row_keeps_the_format_finance_parses() -> None:
    line = Line("Widget", 3, Decimal("9.99"))
    assert export_csv_row(line) == "Widget,3,9.99"
