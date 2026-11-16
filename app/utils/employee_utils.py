
class EmployeeUtils:

    def normalize_employee_data(self, employee_data: dict) -> dict:

        normalized_data = {}

        for key, value in employee_data.items():

            if isinstance(value, str):
                normalized_data[key] = value.strip()

            else:
                normalized_data[key] = value

        return normalized_data


employee_utils = EmployeeUtils()
