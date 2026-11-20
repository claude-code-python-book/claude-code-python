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
