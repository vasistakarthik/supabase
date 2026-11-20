# File-by-File Technical Reference

This document serves as the comprehensive technical encyclopedia for every source code file in the **WORKHUB** project.

---

## 1. app/main.py

- **Purpose**: Master bootstrap file for the FastAPI application.
- **Key Responsibilities**:
  - Initializes FastAPI application instance with custom metadata.
  - Configures global logging via `setup_logging()`.
  - Implements the `@app.on_event("startup")` lifecycle hook to verify PostgreSQL database connectivity.
  - Mounts local static files from `swagger_ui_bundle` under `/swagger-ui`.
  - Implements the custom `/docs` route to serve offline Swagger documentation.
  - Registers `employee_router` and `auth_router`.
  - Provides a root health-check endpoint `GET /`.

---

## 2. app/core/config.py

- **Purpose**: Strongly typed centralized application configuration.
- **Key Responsibilities**:
  - Extends `pydantic_settings.BaseSettings`.
  - Automatically loads and parses `.env` file variables (`DATABASE_URL`, `JWT_SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `DEBUG`, etc.).
  - Instantiates the global singleton `settings = Settings()`.

---

## 3. app/core/dependencies.py

- **Purpose**: Dependency injection providers for FastAPI route handlers.
- **Key Responsibilities**:
  - Implements `get_db() -> Generator[Session, None, None]`.
  - Manages session lifetime: instantiates `SessionLocal()`, yields the session to the calling route, and guarantees execution of `db.close()` in a `finally` block.

---

## 4. app/core/security.py

- **Purpose**: Request-level JWT authorization and user identity verification.
- **Key Responsibilities**:
  - Declares `security_scheme = HTTPBearer()`.
  - Implements `get_current_user(...)` dependency.
  - Extracts the bearer token from the incoming HTTP request.
  - Verifies token validity and expiration via `token_manager`.
  - Queries the database to verify the user exists and has `is_active == True`.
  - Raises `401 Unauthorized` if verification fails.

---

## 5. app/db/connection.py

- **Purpose**: Database engine configuration, sessionmaker factory, and declarative base.
- **Key Responsibilities**:
  - Verifies presence of `settings.DATABASE_URL`.
  - Creates SQLAlchemy engine with `pool_pre_ping=True`.
  - Configures `SessionLocal = sessionmaker(...)`.
  - Defines `class Base(DeclarativeBase)` used by all ORM models.
  - Implements `check_database_connection()` for startup health validation.

---

## 6. app/models/user.py

- **Purpose**: SQLAlchemy ORM representation of the `users` table.
- **Columns**:
  - `id`: Integer primary key (Identity).
  - `email`: Unique String(150), indexed and not nullable.
  - `hashed_password`: String(255) holding the Argon2 hash.
  - `is_active`: Boolean flag defaulting to `True`.

---

## 7. app/models/employee.py

- **Purpose**: SQLAlchemy ORM representation of the `employees` table.
- **Columns**:
  - `id`: BigInteger primary key with SQLite variant mapping for testing.
  - `name`: String(100), not nullable.
  - `email`: String(150), unique, not nullable.
  - `department`: String(100), nullable.
  - `salary`: Numeric(10, 2), nullable.
  - `created_at`: DateTime(timezone=True) with server-side `now()` default.

---

## 8. app/schemas/auth.py

- **Purpose**: Pydantic validation schemas for authentication.
- **Classes**:
  - `RegisterRequest`: Validates incoming `email: EmailStr` and `password: str`.
  - `LoginRequest`: Validates credentials during login.
  - `TokenResponse`: Formats the JWT response (`access_token`, `token_type`).
  - `UserResponse`: Formats user metadata while masking sensitive hashes.

---

## 9. app/schemas/employee.py

- **Purpose**: Pydantic validation schemas for employee operations.
- **Classes**:
  - `EmployeeCreate`: Requires `name`, `email`, optional `department` and `salary`.
  - `EmployeeUpdate`: All fields optional for partial updates.
  - `EmployeeResponse`: Complete representation including `id` and `created_at` with `from_attributes = True` for ORM serialization.

---

## 10. app/repositories/user_repository.py

- **Purpose**: Data access layer for user database operations.
- **Methods**:
  - `get_user_by_email(db, email)`: Fetches a single user record by email.
  - `create_user(db, user_data)`: Persists and refreshes a new User record.

---

## 11. app/repositories/employee_repository.py

- **Purpose**: Data access layer for employee database operations.
- **Methods**:
  - `get_all_employees(db)`: Returns all employee rows.
  - `create_employee(db, employee_data)`: Inserts a new employee.
  - `get_employee_by_id(db, employee_id)`: Fetches employee by primary key.
  - `update_employee(db, employee, employee_data)`: Updates attributes and commits.
  - `delete_employee(db, employee)`: Removes an employee row.

---

## 12. app/services/auth_service.py

- **Purpose**: Business logic layer for user registration and authentication.
- **Methods**:
  - `register(db, register_data)`: Checks for email duplication, hashes the raw password with Argon2, and creates the user.
  - `login(db, login_data)`: Validates credentials, checks active status, verifies password, and generates JWT.

---

## 13. app/services/employee_service.py

- **Purpose**: Business logic layer for employee operations.
- **Methods**:
  - `get_all_employees(db)`: Coordinates retrieval.
  - `create_employee(db, employee_data)`: Normalizes input and saves.
  - `get_employee_by_id(db, employee_id)`: Enforces existence validation (404).
  - `update_employee(db, employee_id, employee_data)`: Applies partial updates.
  - `delete_employee(db, employee_id)`: Deletes and returns confirmation.

---

## 14. app/api/endpoints/auth.py

- **Purpose**: FastAPI route controller for authentication.
- **Endpoints**:
  - `POST /auth/register`: HTTP 201 Created.
  - `POST /auth/login`: HTTP 200 OK.

---

## 15. app/api/endpoints/employees.py

- **Purpose**: FastAPI route controller for employee CRUD.
- **Endpoints**:
  - `GET /employees/`: Read all employees.
  - `POST /employees/`: Create employee.
  - `GET /employees/{id}`: Read employee by ID.
  - `PUT /employees/{id}`: Update employee.
  - `DELETE /employees/{id}`: Delete employee.

---

## 16. app/utils Modules

- **`password_utils.py`**: Encapsulates Argon2 hashing and verification into `PasswordManager`.
- **`token_utils.py`**: Encapsulates PyJWT creation and verification into `TokenManager`.
- **`employee_utils.py`**: Sanitizes string fields (strip, title casing) in `EmployeeUtils`.
- **`performance_utils.py`**: Decorator `@measure_execution_time` logging execution duration.
- **`logging/logging_config.py`**: Configures root logging formatters and handlers.
