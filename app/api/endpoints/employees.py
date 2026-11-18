
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.employee_service import employee_service

from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# 1. GET API - Retrieve all employees
@router.get("/", response_model=list[EmployeeResponse])
def get_all_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return employee_service.get_all_employees(db)


# 2. POST API - Create a new employee
@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=201
)
def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return employee_service.create_employee(
        db,
        employee_data
    )


# 3. GET API - Retrieve employee by ID
@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee_by_id(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return employee_service.get_employee_by_id(
        db,
        employee_id
    )


# 4. PUT API - Update employee details
@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return employee_service.update_employee(
        db,
        employee_id,
        employee_data
    )


# 5. DELETE API - Delete employee
@router.delete(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return employee_service.delete_employee(
        db,
        employee_id
    )
