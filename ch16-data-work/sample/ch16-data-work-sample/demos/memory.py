"""Memory used by text columns, as str and as category."""

import sys
from pathlib import Path

PROJECT = next(
    p / "salesreport"
    for p in Path(__file__).resolve().parents
    if (p / "salesreport").is_dir()
)
sys.path.insert(0, str(PROJECT / "src"))
from salesreport.clean import clean_orders  # noqa: E402
from salesreport.load import read_orders  # noqa: E402
from salesreport.validate import split_valid  # noqa: E402

RAW = PROJECT / "data/raw/orders-2026-10.csv"
valid = split_valid(clean_orders(read_orders(RAW)).orders, "2026-10").valid
for column in ["region", "product", "status"]:
    as_str = valid[column].memory_usage(deep=True, index=False)
    as_cat = valid[column].astype("category").memory_usage(deep=True, index=False)
    print(
        f"{column:<8} {valid[column].nunique():>3} values  "
        f"str {as_str / 1024:7.0f} KiB  category {as_cat / 1024:5.0f} KiB"
    )
