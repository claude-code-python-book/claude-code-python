"""An interactive version of the daily revenue chart, with Plotly Express.

Not run where the book was written (Plotly could not be installed); it
follows the Plotly documentation. tests/extras checks it.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px


def daily_revenue_html(daily: pd.Series, path: Path) -> None:
    """Write a self-contained HTML page that loads Plotly.js from its CDN."""
    frame = pd.DataFrame({"day": daily.index, "revenue": daily.to_numpy() / 100})
    fig = px.bar(frame, x="day", y="revenue", title="Daily revenue (USD)")
    fig.write_html(path, include_plotlyjs="cdn")
