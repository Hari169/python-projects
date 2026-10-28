# Task Management System

## 1. Project Overview

The Task Management System is a command-line application developed using Python and SQLite. It allows users to create, manage, assign, and track tasks through a simple menu-driven interface.

The system implements user authentication and role-based access control to distinguish between administrators and regular users.

## 2. Technologies Used

* Python 3
* SQLite3
* PyCharm IDE

## 3. Features

### User Authentication

* User registration and login.
* Password hashing for secure password storage.
* Separate administrator and regular-user roles.
* Logout functionality.

### Administrator Features

* View registered users.
* View all tasks.
* Create, update, and delete tasks.
* Assign tasks to users.
* Unassign tasks from users.


### Regular User Features

* Create tasks.
* View tasks they created and tasks assigned to them.
* Update and delete tasks they created, subject to permissions.
* Update the status of tasks assigned to them.

### Task Management

* Task title and description.
* Priority levels: Low, Medium, and High.
* Status levels: Pending, In Progress, and Completed.
* Optional due dates.
* Task assignment tracking.

### Database Management

* SQLite database storage.
* Related database tables.
* Foreign-key relationships.
* Input validation and database error handling.

## 4. Project Structure

```text
Task manager/
│
├── main.py
├── database.py
├── auth.py
├── dashboards.py
├── tasks.py
├── projects.py
├── task_management.db
└── README.md
```

## 5. Requirements

* Python 3 installed on your computer.
* No external Python packages are required for the core application.

## 6. How to Run

1. Open the project folder in PyCharm.
2. Configure the Python interpreter.
3. Ensure the required Python files are present.
4. Run `main.py`.
5. Register an account or log in.
6. Use the displayed menu to access the available features.

The SQLite database is initialized automatically when the application starts.

## 7. Database Tables

* **users:** Stores user details, password hashes, and roles.
* **tasks:** Stores task information, priorities, statuses, due dates, and creators.
* **task_assignments:** Records assignments between tasks and users.


## 8. Security and Validation

* Passwords are stored as salted password hashes.
* Parameterized SQL queries are used for database operations.
* Input validation is performed for task IDs, dates, priorities, and statuses.
* Role checks restrict administrative operations.
* Database exceptions are handled to prevent common database errors from terminating the application unexpectedly.

## 9. Conclusion

The Task Management System demonstrates the practical application of Python programming, relational database management, CRUD operations, authentication, role-based access control, and input validation in a command-line application.
