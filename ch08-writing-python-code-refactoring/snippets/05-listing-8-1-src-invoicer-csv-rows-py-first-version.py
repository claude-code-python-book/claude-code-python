"""Read CSV exports from the billing system into plain dictionaries."""

import csv
from collections.abc import Collection
from pathlib import Path


def read_rows(path: Path, required: Collection[str] = ()) -> list[dict[str, str]]:
    """Return the data rows of a CSV export as dictionaries keyed by column.

    Exports come from Excel, so a UTF-8 byte order mark is accepted.
    Whitespace around header names and values is removed, missing trailing
    values become empty strings, and rows with no values at all are skipped.

    Raises:
        ValueError: if a required column is missing, or a row has more
            values than the header has columns.
    """
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = [name.strip() for name in next(reader, [])]
        missing = sorted(set(required) - set(header))
        if missing:
            raise ValueError(f"{path.name}: missing columns: {', '.join(missing)}")
        rows = []
        for number, values in enumerate(reader, start=2):
            if len(values) > len(header):
                raise ValueError(f"{path.name}: row {number} has too many values")
            cleaned = [value.strip() for value in values]
            if not any(cleaned):
                continue
            cleaned += [""] * (len(header) - len(cleaned))
            rows.append(dict(zip(header, cleaned, strict=True)))
    return rows
