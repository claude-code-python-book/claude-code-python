import pandas as pd


def clean(df):
    df.dropna(inplace=True)
    df["region"] = df["region"].apply(lambda r: r.strip().title())
    df["unit_price"] = df["unit_price"].str.replace(",", "").astype(float)
    for i, row in df.iterrows():
        if row["quantity"] <= 0:
            df.drop(i, inplace=True)
    return df.values


if __name__ == "__main__":
    orders = pd.DataFrame({
        "region": [" north", "South", None],
        "quantity": [2, -1, 1],
        "unit_price": ["1,249.00", "49.00", "12.50"],
    })
    clean(orders)
    print(orders)
