import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure not already signed up
    client.delete(f"/activities/{activity}/participants/{email}")
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    # Remove participant
    response3 = client.delete(f"/activities/{activity}/participants/{email}")
    assert response3.status_code == 200
    assert f"Removed {email}" in response3.json()["message"]
    # Remove again should fail
    response4 = client.delete(f"/activities/{activity}/participants/{email}")
    assert response4.status_code == 404

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404

def test_remove_invalid_participant():
    response = client.delete("/activities/Chess Club/participants/notfound@mergington.edu")
    assert response.status_code == 404
