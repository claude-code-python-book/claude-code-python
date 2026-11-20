"""Write a reproducible sample of a raw export for notebooks and Claude.

Usage: python scripts/make_sample.py data/raw/orders-2026-10.csv \
           data/sample/orders-sample.csv 1000
"""

import sys
from pathlib import Path

import pandas as pd


def make_sample(raw: Path, sample: Path, rows: int, seed: int = 16) -> None:
    """Copy a random sample of rows, as text, without touching the raw file."""
    if sample.resolve().parent == raw.resolve().parent:
        raise ValueError("write samples outside the raw data directory")
    frame = pd.read_csv(raw, dtype="str", keep_default_na=False)
    frame.sample(n=rows, random_state=seed).sort_index().to_csv(sample, index=False)


if __name__ == "__main__":
    make_sample(Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]))
