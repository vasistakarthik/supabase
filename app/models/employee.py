
from sqlalchemy import (
    BigInteger,
    Integer,
    String,
    Numeric,
    Identity,
    DateTime,
    func
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.connection import Base


class Employee(Base):

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        Identity(always=True),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    department: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    salary: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
