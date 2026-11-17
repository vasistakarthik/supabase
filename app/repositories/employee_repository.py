
from sqlalchemy.orm import Session

from app.models.employee import Employee


class EmployeeRepository:

    def get_all_employees(self, db: Session):

        return db.query(Employee).all()

    def create_employee(self, db: Session, employee_data: dict):

        employee = Employee(**employee_data)

        db.add(employee)
        db.commit()
        db.refresh(employee)

        return employee

    def get_employee_by_id(self, db: Session, employee_id: int):

        return (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

    def update_employee(
        self,
        db: Session,
        employee: Employee,
        employee_data: dict
    ):

        for key, value in employee_data.items():
            setattr(employee, key, value)

        db.commit()
        db.refresh(employee)

        return employee

    def delete_employee(self, db: Session, employee: Employee):

        db.delete(employee)
        db.commit()

        return employee


employee_repository = EmployeeRepository()
