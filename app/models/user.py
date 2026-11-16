
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:

    email: str
    hashed_password: str
    id: Optional[str] = None
    is_active: bool = True

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "hashed_password": self.hashed_password,
            "is_active": self.is_active
        }
