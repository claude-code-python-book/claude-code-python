"""Revenue by region with Polars, for when the data outgrows pandas.

Not run where the book was written (Polars could not be installed); it
follows the Polars 2 documentation. tests/extras checks it against pandas.
"""

import polars as pl


def revenue_by_region(valid_csv: str) -> pl.DataFrame:
    """Return the same numbers as ``summarize().by_region``."""
    return (
        pl.scan_csv(valid_csv)
        .filter(pl.col("status") == "completed")
        .with_columns(revenue_cents=pl.col("quantity") * pl.col("unit_price_cents"))
        .group_by("region")
        .agg(orders=pl.len(), revenue_cents=pl.col("revenue_cents").sum())
        .sort(["revenue_cents", "region"], descending=[True, False])
        .collect()
    )
