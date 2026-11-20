# System Architecture

## 1. Architectural Philosophy

The **WORKHUB** architecture is built around the **N-Tier (Layered) Architecture Pattern** combined with **Domain-Driven Design (DDD)** concepts and Object-Oriented Principles.

By separating the application into distinct vertical layers, each layer has a single, well-defined responsibility:

- **Zero Business Logic in Controllers**: API endpoints only receive requests, trigger validation, delegate to services, and format responses.
- **Zero SQL / Queries in Services**: Services coordinate logic, validation, and domain rules; they never construct SQL queries directly.
- **Encapsulated Data Access in Repositories**: All database queries (`db.query()`, `db.add()`, `db.commit()`) live exclusively inside Repository classes.
- **Isolated Entities in Models**: Models define database tables and schema structures without leaking business operations.

---

## 2. Layer Diagram

```text
+-------------------------------------------------------------+
|                     Client (Web / Mobile / Swagger)         |
+-------------------------------------------------------------+
                              |
                              | HTTP Requests (JSON)
                              v
+-------------------------------------------------------------+
|                      API Routers Layer                      |
|          app/api/endpoints/auth.py, employees.py            |
|       - Handles HTTP methods (GET, POST, PUT, DELETE)       |
|       - Enforces Dependency Injection (get_db, auth)        |
+-------------------------------------------------------------+
                              |
                              | Validated DTOs (Pydantic Schemas)
                              v
+-------------------------------------------------------------+
|                    Business Services Layer                  |
|          app/services/auth_service.py, employee_service.py  |
|       - Business validations (duplicate checks, rules)      |
|       - Coordinates Utilities (Password, Token, Cleaners)   |
+-------------------------------------------------------------+
                              |
                              | Sanitized Domain Dictionaries
                              v
+-------------------------------------------------------------+
|                 Data Access Repository Layer                |
|      app/repositories/user_repository.py, employee_repo.py  |
|       - Performs CRUD via SQLAlchemy Session                |
|       - Atomic database transactions (commit/refresh)       |
+-------------------------------------------------------------+
                              |
                              | SQLAlchemy ORM Entities
                              v
+-------------------------------------------------------------+
|                     Database Engine Layer                   |
|                   app/db/connection.py                      |
|       - Engine, Connection Pool, and Session Factory        |
+-------------------------------------------------------------+
                              |
                              | TCP / Pooler Connection (Port 5432)
                              v
+-------------------------------------------------------------+
|                  PostgreSQL Database (Supabase)             |
+-------------------------------------------------------------+
```

---

## 3. Core Design Patterns Employed

### 1. Repository Pattern

Data access logic is completely abstracted from the business logic layer.

- `EmployeeRepository` and `UserRepository` wrap all persistence mechanisms.
- If the underlying storage changes or queries need optimization, only the repository changes, leaving services and routers untouched.

### 2. Dependency Injection Pattern

FastAPI's `Depends` system provides clean, modular inversion of control:

- Database sessions (`get_db`) are created per request and guaranteed to be closed when the request completes.
- Security dependencies (`get_current_user`) verify the caller's JWT token before any route code executes.

### 3. Data Transfer Object (DTO) Pattern

Pydantic models act as strongly typed DTOs:

- Separate models for Creation (`EmployeeCreate`), Updates (`EmployeeUpdate`), and Responses (`EmployeeResponse`).
- Sensitive internal fields (such as `hashed_password`) are never exposed in response DTOs (`UserResponse`).

### 4. Singleton Utility Pattern

Cross-cutting concerns (password hashing, token management, logging, data normalization) are encapsulated into standalone classes and instantiated as singletons:

- `password_manager = PasswordManager()`
- `token_manager = TokenManager()`
- `employee_utils = EmployeeUtils()`
- `employee_service = EmployeeService()`
- `auth_service = AuthService()`
