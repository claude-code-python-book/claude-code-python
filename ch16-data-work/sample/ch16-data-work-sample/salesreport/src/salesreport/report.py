"""Turn valid orders into the numbers the monthly report shows."""

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class Summary:
    """Completed orders only. Money is in integer cents."""

    month: str
    orders: int
    revenue_cents: int
    by_region: pd.DataFrame
    top_products: pd.DataFrame
    daily: pd.Series


def summarize(valid: pd.DataFrame, month: str, top: int = 5) -> Summary:
    """Aggregate completed orders by region, product and day."""
    done = valid[valid["status"] == "completed"]
    done = done.assign(revenue_cents=done["quantity"] * done["unit_price_cents"])
    by_region = (
        done.groupby("region", as_index=False)
        .agg(orders=("order_id", "count"), revenue_cents=("revenue_cents", "sum"))
        .sort_values(
            ["revenue_cents", "region"], ascending=[False, True], ignore_index=True
        )
    )
    top_products = (
        done.groupby("product", as_index=False)
        .agg(units=("quantity", "sum"), revenue_cents=("revenue_cents", "sum"))
        .sort_values(
            ["revenue_cents", "product"], ascending=[False, True], ignore_index=True
        )
        .head(top)
    )
    days = pd.date_range(f"{month}-01", periods=1, freq="MS")[0]
    calendar = pd.date_range(days, days + pd.offsets.MonthEnd(0), freq="D")
    daily = (
        done.groupby("order_date")["revenue_cents"]
        .sum()
        .reindex(calendar, fill_value=0)
    )
    return Summary(
        month,
        len(done),
        int(done["revenue_cents"].sum()),
        by_region,
        top_products,
        daily,
    )


def money(cents: int) -> str:
    """Format integer cents as 12,345.67."""
    return f"{cents // 100:,}.{cents % 100:02d}"


def render_markdown(
    summary: Summary, *, rejected: int, duplicates: int, source: str
) -> str:
    """Render the report. No timestamps, so the output is reproducible."""
    average = round(summary.revenue_cents / summary.orders) if summary.orders else 0
    lines = [
        f"# Sales report: {summary.month}",
        "",
        f"Source: `{source}`. Completed orders only; amounts in USD.",
        "",
        f"- Orders: {summary.orders:,}",
        f"- Revenue: {money(summary.revenue_cents)}",
        f"- Average order: {money(average)}",
        f"- Rows rejected: {rejected:,} (see `rejected.csv`)",
        f"- Duplicate rows dropped: {duplicates:,}",
        "",
        "## Revenue by region",
        "",
        "| Region | Orders | Revenue | Share |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in summary.by_region.to_dict("records"):
        share = row["revenue_cents"] / summary.revenue_cents
        lines.append(
            f"| {row['region']} | {row['orders']:,} | "
            f"{money(row['revenue_cents'])} | {share:.1%} |"
        )
    lines += [
        "",
        f"## Top {len(summary.top_products)} products",
        "",
        "| Product | Units | Revenue |",
        "| --- | ---: | ---: |",
    ]
    for row in summary.top_products.to_dict("records"):
        lines.append(
            f"| {row['product']} | {row['units']:,} | {money(row['revenue_cents'])} |"
        )
    lines += ["", "![Daily revenue](daily_revenue.png)", ""]
    return "\n".join(lines)
