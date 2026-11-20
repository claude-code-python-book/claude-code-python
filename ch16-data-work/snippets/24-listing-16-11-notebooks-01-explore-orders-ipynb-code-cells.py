# %% [load]
from pathlib import Path

from salesreport.clean import clean_orders
from salesreport.load import read_orders
from salesreport.report import summarize
from salesreport.validate import split_valid

SAMPLE = Path("../data/sample/orders-sample.csv")
cleaned = clean_orders(read_orders(SAMPLE))
checked = split_valid(cleaned.orders, month="2026-10")
len(checked.valid), len(checked.rejected)

# %% [rejects]
checked.rejected["reason"].value_counts()

# %% [regions]
summarize(checked.valid, "2026-10").by_region
