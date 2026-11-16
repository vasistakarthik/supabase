
from fastapi import APIRouter

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
def get_all_employees():

    employees = employee_service.get_all_employees()

    return employees


# 2. POST API - Create a new employee
@router.post(
    "/",
    response_model=list[EmployeeResponse],
    status_code=201
)
def create_employee(employee_data: EmployeeCreate):

    employee = employee_service.create_employee(employee_data)

    return employee


# 3. GET API - Retrieve employee by ID
@router.get(
    "/{employee_id}",
    response_model=list[EmployeeResponse]
)
def get_employee_by_id(employee_id: int):

    employee = employee_service.get_employee_by_id(employee_id)

    return employee


# 4. PUT API - Update employee details
@router.put(
    "/{employee_id}",
    response_model=list[EmployeeResponse]
)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate
):

    employee = employee_service.update_employee(
        employee_id,
        employee_data
    )

    return employee


# 5. DELETE API - Delete employee
@router.delete(
    "/{employee_id}",
    response_model=list[EmployeeResponse]
)
def delete_employee(employee_id: int):

    employee = employee_service.delete_employee(employee_id)

    return employee
