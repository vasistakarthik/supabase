
from uuid import uuid4

from app.models.user import User
from conftest import TestingSessionLocal


def test_register_and_login(client):

    email = f"test_{uuid4().hex[:8]}@example.com"
    password = "TestPassword123"

    try:
        # 1. Register a new user
        register_response = client.post(
            "/auth/register",
            json={
                "email": email,
                "password": password
            }
        )

        assert register_response.status_code == 201

        # 2. Login with the registered user
        login_response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password
            }
        )

        assert login_response.status_code == 200

        # 3. Verify JWT response
        response_data = login_response.json()

        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"

    finally:
        # 4. Clean up test user from SQLite
        db = TestingSessionLocal()

        try:
            test_user = db.query(User).filter(
                User.email == email
            ).first()

            if test_user:
                db.delete(test_user)
                db.commit()

        finally:
            db.close()


def test_login_with_invalid_password(client):

    response = client.post(
        "/auth/login",
        json={
            "email": f"unknown_{uuid4().hex[:8]}@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401
