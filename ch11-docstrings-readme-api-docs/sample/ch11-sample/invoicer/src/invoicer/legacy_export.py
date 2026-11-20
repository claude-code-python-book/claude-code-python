"""CSV export used by the nightly finance job. Keep signatures stable."""

from invoicer.tax import Line


def export_csv_row(line: Line) -> str:
    """Format one line as `description,quantity,unit_price` for the finance job.

    The values are joined with commas and not quoted, so a description that
    contains a comma adds a column. The nightly job depends on this exact
    format; don't change it without the finance team.
    """
    return f"{line.description},{line.quantity},{line.unit_price}"
