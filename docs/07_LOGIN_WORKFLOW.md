# Login Workflow (`POST /auth/login`)

## 1. Overview

The login endpoint validates user credentials against the stored cryptographic hash and issues a signed, time-limited JSON Web Token (JWT).

- **Endpoint**: `POST /auth/login`
- **Access**: Public
- **HTTP Status Code**: `200 OK`

---

## 2. Request & Response Payload Specification

### Request Payload (`LoginRequest`)

```json
{
  "email": "developer@company.com",
  "password": "StrongPassword123"
}
```

### Response Payload (`TokenResponse`)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 3. Step-by-Step Execution Journey

```text
[Client]
   │  POST /auth/login
   ▼
[app/api/endpoints/auth.py]
   │  Pydantic parses & validates LoginRequest schema
   │  Calls auth_service.login(db, login_data)
   ▼
[app/services/auth_service.py]
   │  Step 1: Fetch user record
   │  Calls user_repository.get_user_by_email(db, email)
   ▼
[app/repositories/user_repository.py]
   │  Runs: SELECT * FROM users WHERE email = :email LIMIT 1
   │  Returns: User object OR None
   ▼
[app/services/auth_service.py]
   │  Step 2: Check existence
   │  If user is None:
   │     raise HTTPException(401 Unauthorized, "Invalid email or password")
   │
   │  Step 3: Check account status
   │  If not user.is_active:
   │     raise HTTPException(403 Forbidden, "User account is inactive")
   │
   │  Step 4: Verify password hash
   │  Calls password_manager.verify_password(raw_password, user.hashed_password)
   │  If verification fails:
   │     raise HTTPException(401 Unauthorized, "Invalid email or password")
   │
   │  Step 5: Generate JWT Token
   │  Calls token_manager.create_access_token(str(user.id))
   ▼
[app/utils/token_utils.py]
   │  Builds payload: {"sub": str(user_id), "exp": now + 30m, "iat": now}
   │  Signs with HS256 algorithm and settings.JWT_SECRET_KEY
   │  Logs: "[INFO] JWT access token generated successfully!"
   │  Returns encoded JWT string
   ▼
[app/services/auth_service.py]
   │  Returns {"access_token": token, "token_type": "bearer"}
   ▼
[Client]
   Receives HTTP 200 OK with Bearer access token
```
