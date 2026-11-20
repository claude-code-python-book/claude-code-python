import pytest

from rowbatch import batch_rows


def test_last_batch_may_be_short() -> None:
    assert list(batch_rows(range(7), 3)) == [(0, 1, 2), (3, 4, 5), (6,)]


def test_exact_accepts_full_batches() -> None:
    assert list(batch_rows(range(6), 3, exact=True)) == [(0, 1, 2), (3, 4, 5)]


def test_exact_rejects_short_last_batch() -> None:
    with pytest.raises(ValueError, match="last batch has 1 rows, expected 3"):
        list(batch_rows(range(7), 3, exact=True))


@pytest.mark.parametrize("size", [0, -1])
def test_size_must_be_positive(size: int) -> None:
    with pytest.raises(ValueError, match="at least 1"):
        batch_rows(range(3), size)


def test_empty_input_gives_no_batches() -> None:
    assert list(batch_rows([], 10, exact=True)) == []
