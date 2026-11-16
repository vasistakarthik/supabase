from app.db.connection import supabase_connection


class EmployeeRepository:

    def __init__(self):
        self.client = supabase_connection.connect()

    def get_all_employees(self):

        response = (
            self.client
            .table("employees")
            .select("*")
            .execute()
        )

        return response.data

    def create_employee(self, employee):

        response = (
            self.client
            .table("employees")
            .insert(employee.to_dict())
            .execute()
        )

        return response.data

    def get_employee_by_id(self, employee_id: int):

        response = (
            self.client
            .table("employees")
            .select("*")
            .eq("id", employee_id)
            .execute()
        )

        return response.data

    def update_employee(self, employee_id: int, employee_data: dict):

        response = (
            self.client
            .table("employees")
            .update(employee_data)
            .eq("id", employee_id)
            .execute()
        )

        return response.data

    def delete_employee(self, employee_id: int):

        response = (
            self.client
            .table("employees")
            .delete()
            .eq("id", employee_id)
            .execute()
        )

        return response.data
        
employee_repository = EmployeeRepository()
