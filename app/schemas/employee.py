
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class EmployeeCreate(BaseModel):

    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    department: Optional[str] = Field(default=None, max_length=100)
    salary: Optional[float] = Field(default=None, ge=0)


class EmployeeUpdate(BaseModel):

    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    department: Optional[str] = Field(default=None, max_length=100)
    salary: Optional[float] = Field(default=None, ge=0)


class EmployeeResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    department: Optional[str] = None
    salary: Optional[float] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
