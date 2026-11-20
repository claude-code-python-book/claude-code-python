"""Split CSV rows into fixed-size batches for bulk inserts."""

from rowbatch.batching import batch_rows
from rowbatch.reader import read_rows

__all__ = ["batch_rows", "read_rows"]
