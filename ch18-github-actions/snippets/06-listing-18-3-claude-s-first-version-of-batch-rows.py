"""Group rows into tuples of a fixed size."""

from collections.abc import Iterable, Iterator
from itertools import batched


def batch_rows[T](
    rows: Iterable[T], size: int, *, exact: bool = False
) -> Iterator[tuple[T, ...]]:
    """Yield tuples of ``size`` rows; with ``exact=True`` all must be full."""
    if size < 1:
        raise ValueError("size must be at least 1")
    return batched(rows, size, strict=exact)
