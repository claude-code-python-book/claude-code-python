"""Three ways pandas gets a value wrong without raising an error."""

import pandas as pd

dates = pd.Series(["2026-10-03", "2026-10-13", "03-10-2026", "2026-10-31"])
print("format='mixed':")
print(pd.to_datetime(dates, format="mixed").dt.strftime("%d %b").tolist())
print("format='mixed', dayfirst=True:")
print(
    pd.to_datetime(dates, format="mixed", dayfirst=True).dt.strftime("%d %b").tolist()
)

prices = pd.Series(["1,249.00", "49.00"])
print("sum of text prices:", repr(prices.sum()))

coerced = pd.to_numeric(pd.Series(["49.00", "N/A", ""]), errors="coerce")
print("coerced sum:", coerced.sum(), "from", coerced.count(), "of 3 values")
