"""Read CSV files into dictionaries."""

import csv
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    """Return the rows of a UTF-8 CSV file with a header line."""
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))
