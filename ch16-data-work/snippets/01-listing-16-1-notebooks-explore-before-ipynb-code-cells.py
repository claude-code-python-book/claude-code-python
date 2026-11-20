# %% [load]
import numpy as np
import pandas as pd

orders = pd.read_csv("../data/sample/orders-sample.csv")
orders.head()

# %% [dtypes]
orders.dtypes

# %% [regions]
orders["region"].value_counts()

# %% [dates]
orders["order_date"] = pd.to_datetime(orders["order_date"], format="mixed")
orders["order_date"].dt.month.value_counts().head(3)

# %% [prices]
orders["unit_price"] = pd.to_numeric(
    orders["unit_price"].str.replace(",", ""), errors="coerce"
)
orders["revenue"] = orders["quantity"] * orders["unit_price"]
orders.groupby("region")["revenue"].sum()
