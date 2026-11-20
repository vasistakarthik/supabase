# Authentication & Security Architecture

## 1. Overview

**WORKHUB** utilizes a stateless **JWT (JSON Web Token)** authentication system combined with **Argon2** cryptographic hashing, adhering to RFC 7519 and modern NIST security guidelines.

---

## 2. Cryptographic Technologies

### 1. Password Hashing with Argon2

In `app/utils/password_utils.py`, the `PasswordManager` utilizes the Argon2 algorithm (via `argon2-cffi` / `pwdlib`):

- Resistant to GPU brute-force attacks and rainbow table attacks.
- Automatically generates unique cryptographic salts for each password.
- Verification uses constant-time string comparison to prevent timing attacks.

### 2. Token Signing with PyJWT

In `app/utils/token_utils.py`, the `TokenManager` signs tokens using **HMAC-SHA256 (HS256)**:

- Signed with the private `JWT_SECRET_KEY` configured in `.env`.
- Default token expiration is **30 minutes** (`ACCESS_TOKEN_EXPIRE_MINUTES`).
- Token Payload Format:

  ```json
  {
    "sub": "1",
    "iat": 1732098000,
    "exp": 1732099800
  }
  ```

---

## 3. The Security Dependency (`app/core/security.py`)

Protected routes depend on `get_current_user`:

```python
security_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = token_manager.verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user
```

---

## 4. Security Guarantees

- **Missing Token**: If the client provides no header, FastAPI halts execution immediately with `403 Forbidden` / `401 Unauthorized`.
- **Expired Token**: If the token timestamp exceeds `exp`, `verify_access_token()` catches the error and returns `None`, producing `401 Unauthorized`.
- **Tampered Token**: If the signature does not match `JWT_SECRET_KEY`, verification fails.
- **Inactive Users**: Even with a valid token, if an admin sets `is_active = False` in the database, subsequent requests are immediately blocked with `401 Unauthorized`.
