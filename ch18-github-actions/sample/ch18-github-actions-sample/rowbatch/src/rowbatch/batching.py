"""Group rows into tuples of a fixed size."""

from collections.abc import Iterable, Iterator
from itertools import batched


def batch_rows[T](
    rows: Iterable[T], size: int, *, exact: bool = False
) -> Iterator[tuple[T, ...]]:
    """Yield tuples of ``size`` rows; the last one may be shorter.

    With ``exact=True``, a short last batch raises ``ValueError`` instead.
    """
    if size < 1:
        raise ValueError("size must be at least 1")
    return _batches(rows, size, exact)


def _batches[T](rows: Iterable[T], size: int, exact: bool) -> Iterator[tuple[T, ...]]:
    # itertools.batched(strict=...) needs Python 3.13; we support 3.12.
    for batch in batched(rows, size):
        if exact and len(batch) != size:
            raise ValueError(f"last batch has {len(batch)} rows, expected {size}")
        yield batch
