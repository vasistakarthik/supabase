# Database & ORM Workflow

## 1. Overview

**WORKHUB** utilizes **SQLAlchemy 2.0** as its Object Relational Mapper (ORM) paired with the modern **`psycopg` (v3)** DBAPI driver. This provides asynchronous-capable, type-safe persistence against cloud-hosted PostgreSQL (Supabase) in production and in-memory SQLite during automated testing.

---

## 2. PostgreSQL Connection Architecture

### 1. Connection String Format

Configured via `.env` with the `postgresql+psycopg` dialect:

```text
DATABASE_URL=postgresql+psycopg://username:password@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres
```

### 2. Connection Pooling & Recycling

In `app/db/connection.py`:

```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)
```

- `pool_pre_ping=True`: Supabase cloud poolers terminate idle TCP sockets after a timeout period. The pre-ping feature emits a lightweight `SELECT 1` test query before handing a pooled socket to a request. If the socket has died, it transparently rebuilds it, preventing connection errors.

---

## 3. Database Session Lifecycle (`get_db`)

Every API request follows a deterministic session lifecycle defined in `app/core/dependencies.py`:

```python
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```text
Request Begins
   │
   ▼
SessionLocal() creates a new SQLAlchemy Session
   │
   ▼
Yielded into the API endpoint via Depends(get_db)
   │
   ▼
Endpoint / Services / Repositories run queries and commit changes
   │
   ▼
Request completes (or throws an unhandled exception)
   │
   ▼
finally block ALWAYS executes -> db.close() returns connection to pool
```

---

## 4. Dual-Database Strategy: Production vs Testing

To maintain production stability without sacrificing test velocity, the application supports two database modes:

| Feature | Production & Local Dev | Automated Test Suite (`pytest`) |
| --- | --- | --- |
| **Engine** | PostgreSQL (Supabase Cloud) | SQLite in-memory (`sqlite://`) |
| **Driver** | `psycopg` (v3) | Built-in Python `sqlite3` |
| **Pool Class** | QueuePool (with pre-ping) | `StaticPool` (single thread memory) |
| **Isolation** | Real persistent data | Fresh schema created & dropped per test fixture |
| **Speed** | Network round-trip (~100-300ms) | Instantaneous in-memory (~10ms) |
| **Cost / Side-Effects** | None | Zero production pollution or quota usage |

### SQLite Cross-Compatibility in Models

In `app/models/employee.py`, the primary key uses SQLAlchemy's variant system:

```python
id: Mapped[int] = mapped_column(
    BigInteger().with_variant(Integer, "sqlite"),
    Identity(always=True),
    primary_key=True
)
```

This enables SQLite to handle auto-incrementing integer IDs without failing on PostgreSQL's identity sequence syntax.
