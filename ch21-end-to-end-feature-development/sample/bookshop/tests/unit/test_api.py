"""The HTTP layer, in-process with FastAPI's TestClient and fake storage."""

import pytest

pytest.importorskip("fastapi")

from fastapi import FastAPI
from fastapi.testclient import TestClient

from bookshop.api import router
from bookshop.service import ReviewService

from fakes import MemoryRepo, MemoryUoW, RecordingQueue


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    repo, log = MemoryRepo(books={1}), []
    app.state.review_service = ReviewService(lambda: MemoryUoW(repo, log),
                                             RecordingQueue(log))
    app.include_router(router)
    return TestClient(app)


def test_post_then_get(client: TestClient) -> None:
    headers = {"X-User-Id": "ana"}
    r = client.post("/books/1/reviews", json={"stars": 4}, headers=headers)
    assert r.status_code == 201
    assert r.json() == {"average": 4.0, "count": 1}
    assert client.get("/books/1/rating").json() == {"average": 4.0, "count": 1}


def test_errors(client: TestClient) -> None:
    def post(book: int, stars: int, user: str | None = "ana") -> int:
        headers = {"X-User-Id": user} if user else {}
        body = {"stars": stars}
        return client.post(f"/books/{book}/reviews", json=body,
                           headers=headers).status_code

    assert post(9, 4) == 404          # unknown book
    assert post(1, 9) == 422          # stars out of range
    assert post(1, 4, user=None) == 422   # missing X-User-Id header
    assert post(1, 4) == 201
    assert post(1, 2) == 409          # second review by the same user
