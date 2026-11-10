import runpy
from pathlib import Path
from unittest.mock import Mock
import uvicorn
import main as calculator

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


@pytest.mark.parametrize("operation", ["add", "subtract", "multiply"])
def test_arithmetic_failure_returns_400(client, monkeypatch, operation):
    failing_operation = Mock(side_effect=ValueError("Calculation failed"))
    monkeypatch.setattr(calculator, operation, failing_operation)

    response = client.post(f"/{operation}", json={"a": 5, "b": 2})

    assert response.status_code == 400
    assert response.json() == {"error": "Calculation failed"}
    failing_operation.assert_called_once_with(5.0, 2.0)


def test_unexpected_division_failure_returns_500(client, monkeypatch):
    failing_divide = Mock(side_effect=RuntimeError("Unexpected failure"))
    monkeypatch.setattr(calculator, "divide", failing_divide)

    response = client.post("/divide", json={"a": 5, "b": 2})

    assert response.status_code == 500
    assert response.json() == {"error": "Internal Server Error"}
    failing_divide.assert_called_once_with(5.0, 2.0)


def test_number_validator_rejects_non_numeric_value():
    # Pydantic rejects invalid input before this after-validator receives it.
    # Call the validator directly to exercise its defensive check.
    with pytest.raises(ValueError, match=r"Both a and b must be numbers\."):
        calculator.OperationRequest.validate_numbers("abc")


def test_running_main_as_script_starts_uvicorn(monkeypatch):
    start_server = Mock()
    monkeypatch.setattr(uvicorn, "run", start_server)

    script = runpy.run_path(str(Path(calculator.__file__)), run_name="__main__")

    start_server.assert_called_once_with(
        script["app"], host="127.0.0.1", port=8000
    )