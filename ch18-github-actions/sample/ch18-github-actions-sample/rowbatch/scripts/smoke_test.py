"""Run against an installed wheel or sdist, not the source tree."""

from importlib.metadata import version

import rowbatch

batches = list(rowbatch.batch_rows(range(5), 2))
assert batches == [(0, 1), (2, 3), (4,)], batches
assert "site-packages" in rowbatch.__file__, rowbatch.__file__
print(f"rowbatch {version('rowbatch')} OK")
