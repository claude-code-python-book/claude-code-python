"""Command-line entry point: rowbatch FILE --size N [--exact]."""

import argparse
from pathlib import Path

from rowbatch.batching import batch_rows
from rowbatch.reader import read_rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rowbatch")
    parser.add_argument("file", type=Path)
    parser.add_argument("--size", type=int, default=500)
    parser.add_argument("--exact", action="store_true")
    args = parser.parse_args(argv)

    rows = read_rows(args.file)
    batches = list(batch_rows(rows, args.size, exact=args.exact))
    print(f"{len(rows)} rows in {len(batches)} batches of up to {args.size}")
    return 0
