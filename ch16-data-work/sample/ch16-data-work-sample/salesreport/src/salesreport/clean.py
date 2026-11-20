"""Normalize the text in an export. Parsing and checking come next."""

from dataclasses import dataclass

import pandas as pd

# "north", "n", "North" -> "North", and the same for the other regions
REGIONS = {
    alias: name
    for name in ("North", "South", "East", "West")
    for alias in (name.lower(), name[0].lower())
}
LEGACY_DATE = r"^(\d{2})-(\d{2})-(\d{4})$"  # DD-MM-YYYY from the old till


@dataclass(frozen=True)
class Cleaned:
    """Cleaned orders plus the number of exact duplicate rows dropped."""

    orders: pd.DataFrame
    duplicates_dropped: int


def clean_orders(raw: pd.DataFrame) -> Cleaned:
    """Return a cleaned copy of ``raw``; ``raw`` itself is never changed."""
    orders = raw.apply(lambda column: column.str.strip())
    lowered = orders["region"].str.lower()
    orders["region"] = lowered.map(REGIONS).fillna(orders["region"])
    orders["status"] = orders["status"].str.lower()
    orders["unit_price"] = orders["unit_price"].str.replace(",", "", regex=False)
    orders["order_date"] = orders["order_date"].str.replace(
        LEGACY_DATE, r"\3-\2-\1", regex=True
    )
    deduped = orders.drop_duplicates().reset_index(drop=True)
    return Cleaned(deduped, len(orders) - len(deduped))
