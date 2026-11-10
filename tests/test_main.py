import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_home_page_returns_html(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")


@pytest.mark.parametrize(
    ("endpoint", "a", "b", "expected"),
    [
        ("/add", 2.5, 3, 5.5),
        ("/subtract", 2, 5, -3),
        ("/multiply", -2, 4, -8),
        ("/divide", 5, 2, 2.5),
    ],
)
def test_calculation_endpoints(client, endpoint, a, b, expected):
    response = client.post(endpoint, json={"a": a, "b": b})

    assert response.status_code == 200
    assert response.json() == {"result": expected}


def test_division_by_zero_returns_400(client):
    response = client.post("/divide", json={"a": 5, "b": 0})

    assert response.status_code == 400
    assert response.json() == {"error": "Cannot divide by zero!"}


@pytest.mark.parametrize(
    ("payload", "invalid_field"),
    [
        ({"b": 2}, "a"),
        ({"a": 2, "b": "abc"}, "b"),
    ],
)
def test_invalid_input_returns_400(client, payload, invalid_field):
    response = client.post("/add", json=payload)

    assert response.status_code == 400
    assert response.json()["error"].startswith(f"{invalid_field}:")