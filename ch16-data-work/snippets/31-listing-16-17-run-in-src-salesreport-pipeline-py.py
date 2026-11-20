def run(source: Path, out_dir: Path, month: str) -> RunResult:
    """Build the report for ``month`` from ``source`` into ``out_dir``."""
    if "raw" in out_dir.resolve().parts:
        raise ValueError(f"refusing to write into raw data: {out_dir}")
    raw = read_orders(source)
    cleaned = clean_orders(raw)
    checked = split_valid(cleaned.orders, month)
    summary = summarize(checked.valid, month)

    out_dir.mkdir(parents=True, exist_ok=True)
    checked.valid.to_csv(out_dir / "orders-valid.csv", index=False)
    checked.rejected.to_csv(out_dir / "rejected.csv", index=False)
    summary.by_region.to_csv(out_dir / "revenue-by-region.csv", index=False)
    plot_daily_revenue(
        summary.daily,
        out_dir / "daily_revenue.png",
        f"Daily revenue, {month} (completed orders)",
    )
    report = render_markdown(
        summary,
        rejected=len(checked.rejected),
        duplicates=cleaned.duplicates_dropped,
        source=source.name,
    )
    (out_dir / "report.md").write_text(report)
    return RunResult(
        len(raw),
        len(checked.valid),
        len(checked.rejected),
        cleaned.duplicates_dropped,
        out_dir,
    )
