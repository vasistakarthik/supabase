# Application Startup Flow

## 1. Overview

When the ASGI server (Uvicorn) starts the application, several critical initialization steps execute deterministically to ensure configuration validity, database connectivity, and offline documentation availability before serving traffic.

---

## 2. Startup Lifecycle Sequence

```text
1. Module Import & Environment Parsing (app.core.config.settings)
   │
   ▼
2. Global Logging Setup (app.utils.logging.logging_config.setup_logging())
   │
   ▼
3. SQLAlchemy Engine & Connection Pool Creation (app.db.connection)
   │
   ▼
4. FastAPI App Instantiation (app.main.app)
   │
   ▼
5. Local Swagger Static Asset Mount (/swagger-ui)
   │
   ▼
6. Router Registration (/employees, /auth)
   │
   ▼
7. Application Startup Event Hook (@app.on_event("startup"))
   │  ├── Check environment (Bypass if APP_ENV == "test")
   │  └── Test PostgreSQL connectivity (check_database_connection())
   │
   ▼
8. Ready to Accept Incoming HTTP Requests on Port 8000
```

---

## 3. Step-by-Step Breakdown

### Step 1: Configuration Loading

- In `app/core/config.py`, the `Settings` class reads `.env` using Pydantic Settings.
- If required variables (like `DATABASE_URL` or `JWT_SECRET_KEY`) are missing, the process fails immediately at boot time with a clear descriptive validation error.

### Step 2: Global Logging Configuration

- `setup_logging()` in `app/utils/logging/logging_config.py` initializes standard Python `logging`.
- It defines the format:

  ```text
  %(asctime)s - %(levelname)s - %(name)s - %(message)s
  ```

- All application loggers inherit this configuration to produce clean, timestamped terminal logs.

### Step 3: Database Engine Creation

- `app/db/connection.py` initializes:

  ```python
  engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
  SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
  ```

- `pool_pre_ping=True` ensures stale or dropped connections in the pool (e.g. from Supabase connection poolers) are transparently recycled before executing queries.

### Step 4: Router & Static Asset Registration

- Static files for Swagger UI from `swagger_ui_bundle` are mounted at `/swagger-ui`.
- `auth_router` and `employee_router` are registered onto the main `app`.

### Step 5: Startup Health Check

- The `@app.on_event("startup")` trigger runs `check_database_connection()`.
- If `APP_ENV != "test"`, an active test connection to PostgreSQL is established.
- If successful, it logs:

  ```text
  [INFO] PostgreSQL connected successfully!
  ```

- If the connection fails (e.g. invalid credentials or network block), it logs an exception trace and halts before serving corrupted traffic.
