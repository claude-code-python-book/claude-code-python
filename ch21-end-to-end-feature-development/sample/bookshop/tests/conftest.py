import pytest

from bookshop.service import ReviewService

from fakes import MemoryRepo, MemoryUoW, RecordingQueue


@pytest.fixture
def log() -> list[str]:
    return []


@pytest.fixture
def repo() -> MemoryRepo:
    return MemoryRepo(books={1, 2})


@pytest.fixture
def service(repo: MemoryRepo, log: list[str]) -> ReviewService:
    return ReviewService(lambda: MemoryUoW(repo, log), RecordingQueue(log))
