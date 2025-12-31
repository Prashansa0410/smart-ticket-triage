from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_ticket_api():
    response = client.post(
        "/tickets",
        json={
            "title": "Login issue",
            "description": "Unable to login with correct password"
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Login issue"
    assert data["status"] == "OPEN"
