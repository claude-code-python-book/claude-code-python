"""The frame-level contract as a Pandera model.

Not run where the book was written (Pandera could not be installed); it
follows the Pandera documentation. tests/extras checks it.
"""

import pandera.pandas as pa
from pandera.typing.pandas import Series


class ValidOrders(pa.DataFrameModel):
    """Columns of orders-valid.csv that the report depends on."""

    order_id: Series[str] = pa.Field(unique=True, str_matches=r"^ORD-\d{6}$")
    region: Series[str] = pa.Field(isin=["North", "South", "East", "West"])
    quantity: Series[int] = pa.Field(gt=0)
    unit_price_cents: Series[int] = pa.Field(gt=0)
    status: Series[str] = pa.Field(isin=["completed", "cancelled", "refunded"])
