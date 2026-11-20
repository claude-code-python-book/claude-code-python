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
