from app.repositories.employee_repository import employee_repository
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.utils.employee_utils import employee_utils

class EmployeeService:

    def __init__(self):
        self.repository = employee_repository

    def get_all_employees(self):

        employees = self.repository.get_all_employees()

        return employees
    def create_employee(self, employee_data: EmployeeCreate):

        employee_dict = employee_data.model_dump()

        normalized_data = employee_utils.normalize_employee_data(
            employee_dict
        )

        employee = Employee(**normalized_data)

        return self.repository.create_employee(employee)

    def get_employee_by_id(self, employee_id: int):

        employee = self.repository.get_employee_by_id(employee_id)

        return employee

    def update_employee(
        self,
        employee_id: int,
        employee_data: EmployeeUpdate
    ):

        update_data = employee_data.model_dump(exclude_unset=True)

        normalized_data = employee_utils.normalize_employee_data(
            update_data
        )

        return self.repository.update_employee(
            employee_id,
            normalized_data
        )

    def delete_employee(self, employee_id: int):

        deleted_employee = self.repository.delete_employee(employee_id)

        return deleted_employee
employee_service = EmployeeService()