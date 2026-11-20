"""Three ways to compute revenue for 20,000 rows, timed."""

import sys
import time
from pathlib import Path

import pandas as pd

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


def best_of(fn, repeat=5):
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        result = fn()
        times.append(time.perf_counter() - start)
    return min(times), result


def with_iterrows():
    return pd.Series(
        [row["quantity"] * row["unit_price_cents"] for _, row in valid.iterrows()],
        index=valid.index,
    )


def with_apply():
    return valid.apply(lambda row: row["quantity"] * row["unit_price_cents"], axis=1)


def vectorized():
    return valid["quantity"] * valid["unit_price_cents"]


results = {}
for name, fn in [
    ("iterrows loop", with_iterrows),
    ("apply(axis=1)", with_apply),
    ("vectorized", vectorized),
]:
    seconds, results[name] = best_of(fn)
    print(f"{name:<15} {seconds * 1000:9.1f} ms")
same = all(results["vectorized"].equals(r.astype("int64")) for r in results.values())
print(f"{len(valid):,} rows; all three agree: {same}")
