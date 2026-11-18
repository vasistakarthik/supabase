
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings


# Create module logger
logger = logging.getLogger(__name__)


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


# Check database connection when requested
def check_database_connection():

    try:
        with engine.connect():
            logger.info("PostgreSQL connected successfully!")

    except Exception:
        logger.exception("PostgreSQL connection failed!")
        raise
