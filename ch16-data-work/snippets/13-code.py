def clean(df):
    df.dropna(inplace=True)
    df["region"] = df["region"].apply(lambda r: r.strip().title())
    df["unit_price"] = df["unit_price"].str.replace(",", "").astype(float)
    for i, row in df.iterrows():
        if row["quantity"] <= 0:
            df.drop(i, inplace=True)
    return df.values
