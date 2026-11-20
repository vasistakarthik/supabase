# WORKHUB API - Project Overview

## 1. Introduction

**WORKHUB** is a production-grade, enterprise-ready RESTful backend API designed for employee management and role-based workforce orchestration. Built with **FastAPI**, **SQLAlchemy 2.0**, and **PostgreSQL (hosted on Supabase)**, the platform adheres strictly to Object-Oriented Programming (OOP) principles, clean architecture, and modern DevOps standards.

---

## 2. Key Features

- **Object-Oriented & N-Tier Architecture**: Strict separation of concerns across Controllers (APIs), Business Logic (Services), Data Access (Repositories), and Entities (Models).
- **Secure Authentication & Authorization**: Stateless JWT (JSON Web Tokens) with Argon2 password hashing and FastAPI Bearer dependency injection.
- **Full Employee CRUD**: Complete Create, Read, Update, and Delete operations with input data sanitization and business validations.
- **Offline & Self-Contained Swagger Documentation**: Customized OpenAPI documentation operating 100% locally without external CDN dependencies.
- **Dual-Database Strategy**:
  - **Production / Development**: High-performance PostgreSQL via Supabase connection pooling and `psycopg` (v3).
  - **Testing**: Lightning-fast in-memory SQLite database for zero-side-effect automated integration testing.
- **Enterprise Observability**: Structured global logging across all modules and operational health-check monitoring at startup.
- **Containerized & Production-Ready**: Ready for deployment with multi-stage `Dockerfile` and `docker-compose.yml`.

---

## 3. Technology Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| **Web Framework** | FastAPI (>= 0.115) | High-performance asynchronous Python web framework |
| **ASGI Server** | Uvicorn (>= 0.30) | Production ASGI web server |
| **ORM & Database** | SQLAlchemy 2.0 + psycopg3 | Type-safe SQL abstraction and connection pooling |
| **Database Provider** | PostgreSQL (Supabase) | Cloud-hosted relational database |
| **Data Validation** | Pydantic v2 | Data parsing, schema validation, and serialization |
| **Configuration** | Pydantic Settings | Environment variable loading from `.env` |
| **Security & Cryptography** | Argon2-cffi + PyJWT | Cryptographic password hashing and JWT token signing |
| **Testing** | Pytest (>= 8.0) | Automated testing with in-memory SQLite fixtures |
| **Containerization** | Docker & Docker Compose | Repeatable, isolated production deployment |

---

## 4. Directory Structure

```text
workhub/
├── app/
│   ├── api/endpoints/        # HTTP API Routers (auth, employees)
│   ├── core/                 # Configuration, dependencies, and security
│   ├── db/                   # Database engine, sessionmaker, and Base
│   ├── models/               # SQLAlchemy Declarative ORM models
│   ├── repositories/         # Database access layer (queries, CRUD)
│   ├── schemas/              # Pydantic request/response validation schemas
│   ├── services/             # Business logic and domain coordination
│   ├── utils/                # Utilities (logging, passwords, tokens, normalization)
│   └── main.py               # Application bootstrap and router registration
├── docs/                     # Comprehensive technical documentation
├── tests/                    # Pytest test cases and conftest fixtures
├── .env.example              # Environment variables template
├── .gitignore                # Git exclusion rules
├── Dockerfile                # Production container specification
├── docker-compose.yml        # Docker service orchestration
├── pyproject.toml            # Tooling configuration (Pytest, Black, Ruff)
├── README.md                 # Project README
└── requirements.txt          # Python dependencies
```

---

## 5. Getting Started Quickstart

### Prerequisites

- Python 3.12+
- Git
- Access to a PostgreSQL instance (e.g. Supabase)

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/vasistakarthik/supabase.git workhub
   cd workhub
   ```

2. **Create and activate a virtual environment:**

   ```powershell
   python -m venv venv
   # On Windows:
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Copy `.env.example` to `.env` and fill in your database credentials and secrets:

   ```bash
   cp .env.example .env
   ```

5. **Run the Application:**

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

6. **Access Interactive Documentation:**
   Open your browser and navigate to `http://127.0.0.1:8000/docs`.

7. **Run Automated Tests:**

   ```bash
   python -m pytest
   ```
