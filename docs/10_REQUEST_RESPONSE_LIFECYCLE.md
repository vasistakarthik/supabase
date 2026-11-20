# Request-Response Lifecycle

## 1. Overview

This document maps the complete journey of an HTTP request as it enters the **WORKHUB** application, flows through the middleware and security layers, executes database operations, and returns an HTTP response to the client.

---

## 2. Complete Lifecycle Flow

```text
[Client (Web, Mobile, Postman, Swagger)]
       │
       │  1. HTTP Request (e.g. GET /employees/ with Bearer Token)
       ▼
[ASGI Web Server: Uvicorn]
       │
       │  2. Converts TCP byte stream into ASGI Request dictionary
       ▼
[FastAPI Core Application: app/main.py]
       │
       │  3. Matches URL path against registered routers
       ▼
[Endpoint Router: app/api/endpoints/employees.py]
       │
       │  4. Resolves Dependency Tree:
       ├───► Depends(get_current_user) in app/core/security.py
       │        ├── Extracts "Authorization: Bearer <token>"
       │        ├── Calls token_manager.verify_access_token() in app/utils/token_utils.py
       │        ├── Decodes and verifies signature & expiration
       │        ├── Queries DB to ensure user.is_active == True
       │        └── Returns authenticated User entity
       │
       └───► Depends(get_db) in app/core/dependencies.py
                ├── Creates new SessionLocal() from app/db/connection.py
                └── Yields active Session `db`
       │
       │  5. Delegates to Business Logic
       ▼
[Service Layer: app/services/employee_service.py]
       │  Executes domain logic, validation, and sanitization
       │  Delegates data query to repository
       ▼
[Repository Layer: app/repositories/employee_repository.py]
       │  Executes SQLAlchemy query: db.query(Employee).all()
       ▼
[Database Engine: app/db/connection.py]
       │  Acquires pre-pinged connection from connection pool
       │  Sends SQL SELECT over TCP to PostgreSQL
       ▼
[PostgreSQL Database (Supabase)]
       │  Returns tabular result set
       ▼
[Repository Layer: app/repositories/employee_repository.py]
       │  Hydrates rows into list of Employee ORM model instances
       ▼
[Service Layer: app/services/employee_service.py]
       │  Applies any business transformations
       ▼
[Endpoint Router: app/api/endpoints/employees.py]
       │  Validates & serializes Employee instances via EmployeeResponse (Pydantic)
       ▼
[FastAPI Serialization & HTTP Response]
       │  6. Converts Python dictionaries to JSON string
       │  7. Sets HTTP headers (Content-Type: application/json, Content-Length)
       │  8. Executes `finally:` block in get_db -> db.close() releases connection
       ▼
[Client]
       Receives HTTP 200 OK with JSON array of employee records
```
