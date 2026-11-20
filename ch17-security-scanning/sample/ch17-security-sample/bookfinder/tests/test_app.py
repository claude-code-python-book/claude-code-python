from starlette.testclient import TestClient

from bookfinder.app import app

client = TestClient(app)


def test_search_returns_json() -> None:
    response = client.get("/search", params={"q": "Okken"})
    assert response.status_code == 200
    assert response.json()["results"][0]["author"] == "Brian Okken"


def test_bad_sort_is_a_client_error() -> None:
    response = client.get("/search", params={"q": "x", "sort": "id--"})
    assert response.status_code == 400


def test_html_page_escapes_the_query() -> None:
    response = client.get("/search.html", params={"q": "<script>alert(1)</script>"})
    assert "<script>" not in response.text
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in response.text
