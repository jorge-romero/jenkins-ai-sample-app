"""Tests for the main FastAPI app.

BUG #5: Some tests have wrong assertions!
"""
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_read_root():
    """Test root endpoint (this one is correct)."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Buggy Sample App!"}


def test_create_user_endpoint():
    """Test create user endpoint.
    
    BUG #5: Wrong status code expectation!
    The endpoint returns 200, but test expects 201.
    """
    response = client.post("/users?name=TestUser&email=test@example.com")
    # OBVIOUS BUG: Wrong assertion! Should be 200, not 201
    assert response.status_code == 200  # Endpoint returns 200 OK
    assert "id" in response.json()


def test_get_user_endpoint():
    """Test get user endpoint (this one is correct)."""
    # First create a user
    response = client.post("/users?name=Alice&email=alice@test.com")
    user_id = response.json()["id"]
    
    # Then get the user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


def test_divide_endpoint():
    """Test division endpoint (this one is correct)."""
    response = client.get("/calculate/divide?a=10&b=2")
    assert response.status_code == 200
    assert response.json()["result"] == 5.0
