# Employee CRUD Workflow

## 1. Overview

The Employee service provides complete CRUD (Create, Read, Update, Delete) management for corporate employee records. All endpoints in this domain are protected by JWT Bearer token authentication.

- **Base Route**: `/employees`
- **Authentication**: Required (`Authorization: Bearer <token>`)

---

## 2. API Operations Matrix

| Method | Endpoint | Description | Request Body | Response Status |
| --- | --- | --- | --- | --- |
| **GET** | `/employees/` | Retrieve all employees | None | `200 OK` (list) |
| **POST** | `/employees/` | Create a new employee | `EmployeeCreate` | `201 Created` |
| **GET** | `/employees/{id}` | Retrieve employee by ID | None | `200 OK` |
| **PUT** | `/employees/{id}` | Update employee details | `EmployeeUpdate` | `200 OK` |
| **DELETE** | `/employees/{id}` | Delete employee record | None | `200 OK` |

---

## 3. Operations In Detail

### 1. Create Employee (`POST /employees/`)

1. Client submits:

   ```json
   {
     "name": "Jane Doe",
     "email": "jane.doe@workhub.io",
     "department": "Engineering",
     "salary": 75000.00
   }
   ```

2. `EmployeeService.create_employee()` invokes `employee_utils.normalize_employee_data(dict)`:
   - Strips leading/trailing whitespace from `name`, `email`, `department`.
   - Normalizes text casing.

3. `EmployeeRepository.create_employee()` persists the record to PostgreSQL and returns the generated `id` and `created_at` timestamp.

### 2. Read All Employees (`GET /employees/`)

1. Router requests `employee_service.get_all_employees(db)`.
2. Repository queries: `db.query(Employee).all()`.
3. Returns a serialized list of `EmployeeResponse` objects.

### 3. Read Employee by ID (`GET /employees/{employee_id}`)

1. Router passes `employee_id: int`.
2. Repository executes: `db.query(Employee).filter(Employee.id == employee_id).first()`.
3. If not found, `EmployeeService` raises:

   ```python
   raise HTTPException(status_code=404, detail="Employee not found")
   ```

### 4. Update Employee (`PUT /employees/{employee_id}`)

1. Client submits partial or complete update fields (`EmployeeUpdate` with optional fields):

   ```json
   {
     "salary": 82000.00
   }
   ```

2. Service fetches existing record; raises `404 Not Found` if missing.
3. Only provided fields (`exclude_unset=True`) are normalized and updated via `setattr(employee, key, value)`.
4. Database changes are committed and refreshed.

### 5. Delete Employee (`DELETE /employees/{employee_id}`)

1. Service verifies record existence via ID.
2. Repository invokes:

   ```python
   db.delete(employee)
   db.commit()
   ```

3. Returns the deleted record representation confirming deletion.
