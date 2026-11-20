"""Small hand-made frames whose right answers can be worked out by hand."""

import pandas as pd
import pytest

from salesreport.load import COLUMNS

# fmt: off
ROWS = [
    # order_id,  order_date,  region,  product,  qty,  price,  status
    ["ORD-000001", "2026-10-01", "North", "Mouse", "2", "49.00", "completed"],
    ["ORD-000002", "02-10-2026", " east", "Desk", "1", "1,249.00", "Completed"],
    ["ORD-000003", "2026-10-02", "N", "Mouse", "1", "49.00", "cancelled"],
    ["ORD-000004", "2026-10-03", "Central", "Mouse", "1", "49.00", "completed"],
    ["ORD-000005", "2026-10-03", "South", "Webcam", "0", "99.00", "completed"],
    ["ORD-000006", "2026-10-04", "South", "Webcam", "1", "N/A", "completed"],
    ["ORD-000007", "2026-09-30", "West", "Mouse", "1", "49.00", "completed"],
    ["ORD-000008", "2026-10-05", "West", "Keyboard", "3", "129.00", "completed"],
    ["ORD-000008", "2026-10-05", "West", "Keyboard", "3", "129.00", "completed"],
    ["ORD-000009", "2026-10-06", "South", "Mouse", "1", "49.00", "refunded"],
    ["ORD-000010", "2026-10-06", "South", "Mouse", "1", "49.00", "completed"],
    ["ORD-000010", "2026-10-06", "South", "Mouse", "2", "49.00", "completed"],
]
# fmt: on


@pytest.fixture
def raw() -> pd.DataFrame:
    """Twelve raw rows as the export writes them: all text."""
    return pd.DataFrame(ROWS, columns=COLUMNS, dtype="str")
