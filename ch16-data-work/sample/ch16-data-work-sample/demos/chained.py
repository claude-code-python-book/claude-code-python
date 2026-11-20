import pandas as pd

orders = pd.DataFrame({"region": ["North", "South"], "quantity": [2, -1]})
orders[orders["quantity"] < 0]["quantity"] = 0
print(orders["quantity"].tolist())
orders.loc[orders["quantity"] < 0, "quantity"] = 0
print(orders["quantity"].tolist())
