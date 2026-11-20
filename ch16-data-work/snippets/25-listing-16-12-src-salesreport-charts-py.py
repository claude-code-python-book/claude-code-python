"""Static charts for the report, drawn with matplotlib."""

from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")  # draw to files only; no window needed

import matplotlib.pyplot as plt
import pandas as pd


def plot_daily_revenue(daily: pd.Series, path: Path, title: str) -> None:
    """Save a bar chart of revenue per day (daily values are in cents)."""
    fig, ax = plt.subplots(figsize=(8, 3.6), layout="constrained")
    try:
        ax.bar(daily.index, daily.to_numpy() / 100, color="#555555", width=0.8)
        ax.set_title(title, loc="left", fontsize=11)
        ax.set_ylabel("Revenue (USD)")
        ax.yaxis.set_major_formatter("{x:,.0f}")
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#dddddd", linewidth=0.6)
        ax.set_axisbelow(True)
        ticks = daily.index[daily.index.day.isin([1, 8, 15, 22, 29])]
        ax.set_xticks(ticks, [day.strftime("%d %b") for day in ticks])
        fig.savefig(path, dpi=200)
    finally:
        plt.close(fig)
