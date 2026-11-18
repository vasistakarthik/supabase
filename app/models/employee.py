
from dataclasses import dataclass
from typing import Optional


@dataclass
class Employee:

    name: str
    email: str
    department: Optional[str] = None
    salary: Optional[float] = None
    id: Optional[int] = None

    def to_dict(self) -> dict:

        return {
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "salary": self.salary
        }
