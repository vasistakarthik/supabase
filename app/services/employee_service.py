
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.employee_repository import employee_repository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.utils.employee_utils import employee_utils
from app.utils.performance_utils import measure_execution_time

class EmployeeService:

    def __init__(self):
        self.repository = employee_repository

    # GET all employees
    @measure_execution_time
    def get_all_employees(self, db: Session):

        return self.repository.get_all_employees(db)

    # CREATE employee
    @measure_execution_time
    def create_employee(
        self,
        db: Session,
        employee_data: EmployeeCreate
    ):

        employee_dict = employee_data.model_dump()

        normalized_data = employee_utils.normalize_employee_data(
            employee_dict
        )

        return self.repository.create_employee(
            db,
            normalized_data
        )

    # GET employee by ID
    @measure_execution_time
    def get_employee_by_id(
        self,
        db: Session,
        employee_id: int
    ):

        employee = self.repository.get_employee_by_id(
            db,
            employee_id
        )

        if employee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        return employee

    # UPDATE employee
    @measure_execution_time
    def update_employee(
        self,
        db: Session,
        employee_id: int,
        employee_data: EmployeeUpdate
    ):

        employee = self.get_employee_by_id(
            db,
            employee_id
        )

        update_data = employee_data.model_dump(
            exclude_unset=True
        )

        normalized_data = employee_utils.normalize_employee_data(
            update_data
        )

        return self.repository.update_employee(
            db,
            employee,
            normalized_data
        )

    # DELETE employee
    @measure_execution_time
    def delete_employee(
        self,
        db: Session,
        employee_id: int
    ):

        employee = self.get_employee_by_id(
            db,
            employee_id
        )

        return self.repository.delete_employee(
            db,
            employee
        )


employee_service = EmployeeService()
