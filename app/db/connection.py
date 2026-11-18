
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings


# Check database URL
if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL is missing")


# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)


# Create database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


# Base class for database models
class Base(DeclarativeBase):
    pass

try:
    with engine.connect() as connection:
        print("PostgreSQL connected successfully!")
except Exception as e:
    print("PostgreSQL connection failed!")
    raise