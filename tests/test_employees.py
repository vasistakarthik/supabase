
from uuid import uuid4

from app.models.employee import Employee
from app.models.user import User
from conftest import TestingSessionLocal


def test_employee_crud(client):

    user_email = f"user_{uuid4().hex[:8]}@example.com"
    employee_email = f"employee_{uuid4().hex[:8]}@example.com"
    password = "TestPassword123"

    try:
        # 1. Register a test user
        register_response = client.post(
            "/auth/register",
            json={
                "email": user_email,
                "password": password
            }
        )

        assert register_response.status_code == 201

        # 2. Login and get access token
        login_response = client.post(
            "/auth/login",
            json={
                "email": user_email,
                "password": password
            }
        )

        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # 3. Create employee
        create_response = client.post(
            "/employees/",
            json={
                "name": "Test Employee",
                "email": employee_email,
                "department": "Testing",
                "salary": 30000
            },
            headers=headers
        )

        assert create_response.status_code == 201

        employee_id = create_response.json()["id"]

        assert isinstance(employee_id, int)

        # 4. Get all employees
        list_response = client.get(
            "/employees/",
            headers=headers
        )

        assert list_response.status_code == 200

        assert any(
            employee["email"] == employee_email
            for employee in list_response.json()
        )

        # 5. Get employee by ID
        get_response = client.get(
            f"/employees/{employee_id}",
            headers=headers
        )

        assert get_response.status_code == 200
        assert get_response.json()["email"] == employee_email

        # 6. Update employee
        update_response = client.put(
            f"/employees/{employee_id}",
            json={
                "name": "Updated Test Employee",
                "department": "Development",
                "salary": 35000
            },
            headers=headers
        )

        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated Test Employee"

        # 7. Delete employee
        delete_response = client.delete(
            f"/employees/{employee_id}",
            headers=headers
        )

        assert delete_response.status_code == 200

    finally:
        # 8. Clean up test records from SQLite
        db = TestingSessionLocal()

        try:
            test_employee = db.query(Employee).filter(
                Employee.email == employee_email
            ).first()

            if test_employee:
                db.delete(test_employee)

            test_user = db.query(User).filter(
                User.email == user_email
            ).first()

            if test_user:
                db.delete(test_user)

            db.commit()

        finally:
            db.close()
