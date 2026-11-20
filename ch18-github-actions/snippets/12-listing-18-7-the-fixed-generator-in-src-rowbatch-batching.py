def _batches[T](rows: Iterable[T], size: int, exact: bool) -> Iterator[tuple[T, ...]]:
    # itertools.batched(strict=...) needs Python 3.13; we support 3.12.
    for batch in batched(rows, size):
        if exact and len(batch) != size:
            raise ValueError(f"last batch has {len(batch)} rows, expected {size}")
        yield batch
