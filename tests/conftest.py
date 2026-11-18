
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from app.main import app
from app.db.connection import Base
from app.core.dependencies import get_db

# Import models to register their database tables
from app.models.employee import Employee
from app.models.user import User


# Create SQLite in-memory database
SQLALCHEMY_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False
)


# Override the original database dependency
def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# Create test database and API client
@pytest.fixture
def client():

    Base.metadata.create_all(bind=test_engine)

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

    Base.metadata.drop_all(bind=test_engine)
