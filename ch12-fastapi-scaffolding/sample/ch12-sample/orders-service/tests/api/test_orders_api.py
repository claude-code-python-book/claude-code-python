from fastapi.testclient import TestClient

LINE = {"sku": "MUG-01", "quantity": 2, "unit_price": "4.50"}
ORDER = {"currency": "GBP", "lines": [LINE]}


def test_place_order_returns_201_and_a_location(as_alice: TestClient) -> None:
    response = as_alice.post("/orders", json=ORDER)
    assert response.status_code == 201
    assert response.headers["location"] == "/orders/1"
    body = response.json()
    assert (body["customer_id"], body["status"], body["total"]) == (
        "C-1001",
        "pending",
        "9.00",
    )


def test_list_is_newest_first_and_paged(as_alice: TestClient) -> None:
    for _ in range(3):
        as_alice.post("/orders", json=ORDER)
    body = as_alice.get("/orders", params={"limit": 2}).json()
    assert [o["id"] for o in body["items"]] == [3, 2]
    assert (body["count"], body["limit"], body["offset"]) == (3, 2, 0)


def test_status_filter_uses_the_status_query_parameter(as_alice: TestClient) -> None:
    as_alice.post("/orders", json=ORDER)
    as_alice.post("/orders", json=ORDER)
    as_alice.post("/orders/1/pay")
    body = as_alice.get("/orders", params={"status": "paid"}).json()
    assert [o["id"] for o in body["items"]] == [1]


def test_unknown_order_is_a_404_problem(as_alice: TestClient) -> None:
    response = as_alice.get("/orders/99")
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/problem+json"
    assert response.json()["instance"] == "/orders/99"


def test_cancelling_twice_is_a_409(as_alice: TestClient) -> None:
    as_alice.post("/orders", json=ORDER)
    assert as_alice.post("/orders/1/cancel").status_code == 200
    assert as_alice.post("/orders/1/cancel").status_code == 409


def test_duplicate_skus_are_a_422(as_alice: TestClient) -> None:
    response = as_alice.post("/orders", json={"currency": "GBP", "lines": [LINE, LINE]})
    assert response.status_code == 422
    assert "each SKU may appear once" in response.json()["detail"][0]["msg"]


def test_limit_above_100_is_a_422(as_alice: TestClient) -> None:
    assert as_alice.get("/orders", params={"limit": 101}).status_code == 422
