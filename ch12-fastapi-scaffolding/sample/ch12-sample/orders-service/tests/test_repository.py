from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

from orders.domain import Line
from orders.repository import InMemoryOrderRepository
from tests.conftest import NOW


def test_ids_stay_unique_when_threads_add_at_once() -> None:
    repo = InMemoryOrderRepository()
    line = Line("MUG-01", 1, Decimal("4.50"))

    def add(_: int) -> int:
        return repo.add("C-1001", "GBP", [line], NOW).id

    with ThreadPoolExecutor(max_workers=8) as pool:
        ids = list(pool.map(add, range(2000)))

    assert sorted(ids) == list(range(1, 2001))
