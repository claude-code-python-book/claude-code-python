"""Generate the fake October 2026 shop export used by the examples.

The file imitates a real export, including its faults: inconsistent region
names, a legacy till that writes dates as DD-MM-YYYY, prices with thousands
separators, bad quantities and duplicated rows. Run once; the output is then
treated as raw data and never modified.
"""

import csv
import random
import sys
from datetime import date, timedelta
from pathlib import Path

PRODUCTS = {
    "Standing Desk": 124900,
    "Office Chair": 89900,
    "Whiteboard": 34900,
    "USB-C Dock": 27900,
    "Monitor Arm": 18900,
    "Headset": 15900,
    "Keyboard": 12900,
    "Webcam": 9900,
    "Desk Lamp": 5990,
    "Mouse": 4900,
    "Cable Kit": 2400,
    "Notebook Pack": 1250,
}
REGIONS = ["North", "South", "East", "West"]
MESSY = {
    "North": ["north", " North", "NORTH", "N"],
    "South": ["south", "SOUTH "],
    "East": ["east", "E"],
    "West": ["west", "West "],
}


def price_text(cents: int) -> str:
    return f"{cents / 100:,.2f}"


def make_rows(n: int, rng: random.Random) -> list[list[str]]:
    rows: list[list[str]] = []
    start = date(2026, 10, 1)
    names = list(PRODUCTS)
    weights = [3, 4, 2, 5, 6, 6, 9, 6, 8, 10, 7, 9]
    for i in range(n):
        region = rng.choices(REGIONS, weights=[30, 25, 25, 20])[0]
        day = start + timedelta(days=rng.randrange(31))
        product = rng.choices(names, weights=weights)[0]
        status = rng.choices(["completed", "cancelled", "refunded"], [88, 7, 5])[0]
        order_date = day.isoformat()
        if region == "East" and rng.random() < 0.4:  # the legacy till
            order_date = day.strftime("%d-%m-%Y")
        region_text = region
        if rng.random() < 0.05:
            region_text = rng.choice(MESSY[region])
        if rng.random() < 0.003:
            region_text = rng.choice(["Central", ""])
        if rng.random() < 0.002:
            order_date = "2026-09-30"
        quantity = str(rng.choices([1, 2, 3, 4, 5], [50, 25, 12, 8, 5])[0])
        if rng.random() < 0.003:
            quantity = rng.choice(["0", "-1"])
        price = price_text(PRODUCTS[product])
        if rng.random() < 0.002:
            price = rng.choice(["", "N/A"])
        if rng.random() < 0.02:
            status = status.capitalize()
        rows.append(
            [
                f"ORD-{100000 + i}",
                order_date,
                region_text,
                product,
                quantity,
                price,
                status,
            ]
        )
    for _ in range(n // 100):  # export glitch: exact duplicate rows
        rows.insert(rng.randrange(len(rows)), list(rng.choice(rows)))
    for _ in range(6):  # the same order ID with different contents
        twin = list(rng.choice(rows))
        twin[4] = str(int(twin[4]) + 1) if twin[4].isdigit() else "2"
        rows.insert(rng.randrange(len(rows)), twin)
    return rows


def main(path: str, n: int = 20_000) -> None:
    rows = make_rows(n, random.Random(16))
    with Path(path).open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "order_id",
                "order_date",
                "region",
                "product",
                "quantity",
                "unit_price",
                "status",
            ]
        )
        writer.writerows(rows)


if __name__ == "__main__":
    main(sys.argv[1])
