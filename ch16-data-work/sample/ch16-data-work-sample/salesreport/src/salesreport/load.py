"""Read an order export exactly as written, with no type guessing."""

from pathlib import Path

import pandas as pd

COLUMNS = "order_id order_date region product quantity unit_price status".split()


def read_orders(path: Path, nrows: int | None = None) -> pd.DataFrame:
    """Read every column as text; parsing happens later, where it is tested.

    Empty cells stay as empty strings instead of becoming NaN.
    """
    frame = pd.read_csv(path, dtype="str", keep_default_na=False, nrows=nrows)
    missing = set(COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f"{path.name} is missing columns: {sorted(missing)}")
    return frame[COLUMNS]
