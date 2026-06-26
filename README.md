Employee Management System
Technical Documentation & System Overview
Version 1.0  |  Django REST Framework + Vanilla JS Frontend

1. System Overview
The Employee Management System (EMS) is a full-stack web application built to manage core HR operations within an organisation. It follows a REST API architecture with a Django backend and a lightweight HTML/JavaScript frontend.

The system is structured as two independent layers:
•	Backend — Django 4.x with Django REST Framework (DRF), handling all business logic and data persistence.
•	Frontend — Vanilla HTML, CSS, and JavaScript that consumes the backend REST API.

The database used is SQLite (development mode), making it easy to set up locally without any additional database server.

2. Technology Stack
Layer	Technology	Purpose
Backend	Python / Django 4.x	Core application logic
API Layer	Django REST Framework	RESTful API endpoints
Authentication	SimpleJWT	JWT token-based auth
CORS	django-cors-headers	Cross-origin request handling
Database	SQLite3	Local data persistence
Frontend	HTML / CSS / JavaScript	User interface

3. Project Structure
The repository is split into two root directories:

employee-management-system-main/
├── backend/                  # Django project root
│   ├── accounts/             # User auth & roles module
│   ├── employees/            # Employee & department module
│   ├── attendance/           # Attendance tracking module
│   ├── payroll/              # Payroll management module
│   ├── backend/              # Project config (settings, urls, wsgi)
│   └── manage.py
└── frontend/                 # Standalone HTML/JS frontend
    ├── index.html
    ├── script.js
    └── style.css

4. Module Breakdown
4.1 Accounts Module
Handles user authentication and role-based access control.

User Model
Extends Django's built-in AbstractUser with a custom role field:

Field	Type	Description
username	CharField (inherited)	Unique login identifier
password	CharField (inherited)	Hashed user password
email	EmailField (inherited)	User email address
role	CharField (choices)	ADMIN | HR | EMPLOYEE

Authentication
Login is handled via JWT (JSON Web Tokens) using djangorestframework-simplejwt:
•	POST /api/auth/login/ — accepts username + password, returns access & refresh tokens.
•	The LoginView extends TokenObtainPairView with AllowAny permission (public endpoint).
•	All other endpoints require a valid JWT bearer token in the Authorization header.
4.2 Employees Module
Manages the core employee records and department structure.

Department Model
Field	Type	Description
id	Auto BigInt	Primary key
name	CharField(100)	Department name

Employee Model
Field	Type	Description
employee_code	CharField(20)	Unique employee identifier
user	OneToOneField → User	Linked user account
department	ForeignKey → Department	Assigned department (nullable)
designation	CharField(100)	Job title / role
joining_date	DateField	Date of joining

API Endpoints (Employees)
•	GET /employees/ — list all employees
•	POST /employees/ — create a new employee
•	GET /employees/{id}/ — retrieve a specific employee
•	PUT/PATCH /employees/{id}/ — update employee details
•	DELETE /employees/{id}/ — remove an employee
•	GET /departments/ — list all departments (same CRUD pattern)
4.3 Attendance Module
Tracks daily check-in and check-out times for each employee.

Attendance Model
Field	Type	Description
employee	ForeignKey → Employee	Which employee
date	DateField (auto)	Auto-set to today on creation
check_in	TimeField	Time of arrival
check_out	TimeField (nullable)	Time of departure (optional)

API Endpoints (Attendance)
•	GET /attendance/ — list all attendance records
•	POST /attendance/ — log a check-in for an employee
•	PUT/PATCH /attendance/{id}/ — update record (e.g. log check-out time)
•	DELETE /attendance/{id}/ — remove a record
4.4 Payroll Module
Stores monthly salary information for each employee.

Payroll Model
Field	Type	Description
employee	ForeignKey → Employee	Employee this record belongs to
month	IntegerField	Month number (1–12)
year	IntegerField	Payroll year (e.g. 2025)
net_salary	FloatField	Final net salary amount

API Endpoints (Payroll)
•	GET /payroll/ — list all payroll records
•	POST /payroll/ — create a payroll record for a month
•	GET /payroll/{id}/ — get a specific record
•	PUT/PATCH /payroll/{id}/ — update a payroll record
•	DELETE /payroll/{id}/ — remove a payroll record

Note: The Payroll module uses SessionAuthentication in addition to the standard JWT/IsAuthenticated pattern used across other modules.

5. System Flow
5.1 Authentication Flow
•	Step 1 — User submits username and password to POST /api/auth/login/.
•	Step 2 — Server validates credentials and returns a JWT access token and refresh token.
•	Step 3 — The client stores the token and attaches it as a Bearer token on all subsequent API requests.
•	Step 4 — Protected endpoints validate the token via DRF's IsAuthenticated permission class.

5.2 Employee Lifecycle Flow
•	An Admin or HR user creates a User account (with role = EMPLOYEE).
•	An Employee record is then linked to that user via a OneToOne relationship.
•	A Department is assigned to the employee at creation or updated later.
•	The employee can then have Attendance and Payroll records associated with their Employee ID.

5.3 Attendance Recording Flow
•	Step 1 — An authorised user (HR/Admin) POSTs an attendance record with employee ID and check_in time.
•	Step 2 — The date field is automatically set to today by Django (auto_now_add=True).
•	Step 3 — When the employee leaves, the same record is PATCHed with the check_out time.

5.4 Payroll Generation Flow
•	Step 1 — HR/Admin POSTs a payroll entry with employee ID, month, year, and net_salary.
•	Step 2 — The record is stored and retrievable via the /payroll/ endpoint.
•	Step 3 — The frontend demo calls GET /payroll/ and displays all salary records in formatted JSON.

5.5 Frontend Flow
•	The frontend is a single HTML page (index.html) served statically.
•	A 'Load Payroll' button triggers a fetch() call to http://127.0.0.1:8000/payroll/.
•	The response JSON is formatted and displayed in a <pre> block on the page.
•	No login UI is implemented in the frontend — the backend API must be accessed directly or via a tool like Postman for authenticated operations.

6. Complete API Endpoint Summary
Method	Endpoint	Auth	Description
POST	/api/auth/login/	Public	Get JWT tokens
GET/POST	/employees/	JWT Required	List / create employees
GET/PUT/DEL	/employees/{id}/	JWT Required	Read / update / delete employee
GET/POST	/departments/	JWT Required	List / create departments
GET/PUT/DEL	/departments/{id}/	JWT Required	Read / update / delete department
GET/POST	/attendance/	JWT Required	List / log attendance
GET/PUT/DEL	/attendance/{id}/	JWT Required	Read / update / delete record
GET/POST	/payroll/	Session + JWT	List / create payroll entries
GET/PUT/DEL	/payroll/{id}/	Session + JWT	Read / update / delete payroll

7. User Roles & Permissions
The system defines three user roles via the accounts.User model. Role-based access control is not yet enforced at the view level — all authenticated users currently have full CRUD access. Roles are stored for future permission enforcement.

Role	Intended Responsibilities
ADMIN	Full system access — manage users, employees, payroll, attendance
HR	Manage employee records, attendance logging, payroll entry
EMPLOYEE	Read-only access to own records (future implementation)

8. Local Setup Guide
8.1 Backend Setup
•	Clone the repository and navigate to the backend/ directory.
•	Create a virtual environment and install dependencies:

pip install django djangorestframework djangorestframework-simplejwt django-cors-headers

•	Run database migrations:

python manage.py migrate

•	Create a superuser (Admin account):

python manage.py createsuperuser

•	Start the development server:

python manage.py runserver

The backend will be available at http://127.0.0.1:8000/

8.2 Frontend Setup
•	Open frontend/index.html directly in a browser.
•	Ensure the backend server is running at http://127.0.0.1:8000.
•	Click 'Load Payroll' to fetch and display payroll data from the API.

9. Known Limitations & Future Improvements
•	Role-based permissions are defined but not enforced at the API view level — all authenticated users have equal access.
•	The frontend has no login form; authentication is not wired into the UI.
•	No salary breakdown model (basic pay, deductions, allowances) — only net_salary is stored.
•	No leave management module.
•	SQLite is used for development; should be migrated to PostgreSQL for production.
•	The SECRET_KEY in settings.py is hard-coded and marked as insecure — must be replaced before deployment.
•	CORS is configured to allow all origins (CORS_ALLOW_ALL_ORIGINS = True) — should be restricted in production.
•	No automated tests implemented (test files are empty stubs).

Employee Management System — Internal Documentation
