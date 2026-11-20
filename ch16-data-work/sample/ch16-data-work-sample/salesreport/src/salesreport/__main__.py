"""Command line: python -m salesreport SOURCE --month YYYY-MM --out DIR."""

import argparse
from pathlib import Path

from salesreport.pipeline import run


def main(argv: list[str] | None = None) -> None:
    """Parse arguments, run the pipeline and print a one-line summary."""
    parser = argparse.ArgumentParser(prog="salesreport")
    parser.add_argument("source", type=Path)
    parser.add_argument("--month", required=True, help="for example 2026-10")
    parser.add_argument("--out", type=Path, default=Path("out"))
    args = parser.parse_args(argv)
    result = run(args.source, args.out, args.month)
    print(
        f"read {result.rows_read:,} rows: {result.valid:,} valid, "
        f"{result.rejected:,} rejected, {result.duplicates_dropped:,} "
        f"duplicates dropped -> {result.out_dir}/report.md"
    )


if __name__ == "__main__":
    main()
