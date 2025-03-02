"""End-to-end tests for the route of the FastAPI app"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_coverage_valid_address():
    """Test coverage route with a valid address"""
    response = client.get(
        "/coverage", params={"address": "42 Rue papernest 75011, Paris"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "Orange": {"2G": True, "3G": True, "4G": False},
        "SFR": {"2G": True, "3G": False, "4G": False},
    }


def test_coverage_invalid_address():
    """Test coverage route with an invalid address"""
    response = client.get("/coverage", params={"address": "INVALID_ADDRESS_12345"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Unable to get coordinates for the given address"
    }
