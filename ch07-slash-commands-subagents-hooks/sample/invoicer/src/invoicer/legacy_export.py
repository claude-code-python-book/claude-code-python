"""CSV export used by the nightly finance job. Keep signatures stable."""

from invoicer.tax import Line


def export_csv_row(line: Line) -> str:
    return f"{line.description},{line.quantity},{line.unit_price}"
