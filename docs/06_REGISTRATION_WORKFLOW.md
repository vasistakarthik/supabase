# Registration Workflow (`POST /auth/register`)

## 1. Overview

The registration endpoint creates a new system user with hashed credentials and creates a persistent record in the `users` PostgreSQL table.

- **Endpoint**: `POST /auth/register`
- **Access**: Public
- **HTTP Status Code**: `201 Created`

---

## 2. Request & Response Payload Specification

### Request Payload (`RegisterRequest`)

```json
{
  "email": "developer@company.com",
  "password": "StrongPassword123"
}
```

### Response Payload (`UserResponse`)

```json
{
  "id": 1,
  "email": "developer@company.com",
  "is_active": true
}
```

*(Notice: The password and password hash are strictly excluded from the response schema).*

---

## 3. Step-by-Step Execution Journey

```text
[Client]
   │  POST /auth/register
   ▼
[app/api/endpoints/auth.py]
   │  Pydantic parses & validates RegisterRequest schema (valid email format, min length)
   │  Calls auth_service.register(db, register_data)
   ▼
[app/services/auth_service.py]
   │  Step 1: Check existing user
   │  Calls user_repository.get_user_by_email(db, email)
   ▼
[app/repositories/user_repository.py]
   │  Runs: SELECT * FROM users WHERE email = :email LIMIT 1
   │  Returns: None (if email is free) OR User object (if taken)
   ▼
[app/services/auth_service.py]
   │  Step 2: If taken -> raise HTTPException(409 Conflict, "Email already registered")
   │  Step 3: Hash password
   │  Calls password_manager.hash_password(raw_password) via Argon2
   │  Prepares dictionary: {"email": email, "hashed_password": hash, "is_active": True}
   │  Calls user_repository.create_user(db, user_data)
   ▼
[app/repositories/user_repository.py]
   │  Instantiates User(**user_data)
   │  db.add(user)
   │  db.commit()      <-- Persisted in PostgreSQL
   │  db.refresh(user) <-- Retrieves generated identity ID
   │  Returns created User ORM instance
   ▼
[app/api/endpoints/auth.py]
   │  FastAPI serializes User ORM instance into UserResponse DTO
   ▼
[Client]
   Receives HTTP 201 Created with {id, email, is_active}
```
