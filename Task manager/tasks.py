import sqlite3
from datetime import datetime

DATABASE_NAME = "task_management.db"


def create_task(user):
    print("\n===== CREATE TASK =====")

    title = input("Enter task title: ").strip()
    description = input("Enter task description: ").strip()

    print("\nPriority:")
    print("1. Low")
    print("2. Medium")
    print("3. High")

    priority_options = {
        "1": "Low",
        "2": "Medium",
        "3": "High"
    }

    priority_choice = input("Choose priority: ").strip()

    if priority_choice not in priority_options:
        print("Invalid priority!")
        return

    priority = priority_options[priority_choice]

    due_date = input(
        "Enter due date (YYYY-MM-DD), or leave blank: "
    ).strip()

    # Validate title
    if not title:
        print("Task title cannot be empty!")
        return

    # Validate due date
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date! Use YYYY-MM-DD.")
            return

    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            conn.execute("PRAGMA foreign_keys = ON")

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO tasks
                    (title, description, priority, due_date, created_by)
                VALUES (?, ?, ?, ?, ?)
            """, (
                title,
                description,
                priority,
                due_date or None,
                user["user_id"]
            ))

        print("Task created successfully!")

    except sqlite3.Error as error:
        print("Database error:", error)

def update_task(user):
    print("\n===== UPDATE TASK =====")

    task_id = input("Enter task ID: ").strip()

    if not task_id.isdigit() or int(task_id) <= 0:
        print("Invalid task ID!")
        return

    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT title, description, priority, due_date, status
                FROM tasks
                WHERE task_id = ?
            """, (int(task_id),))

            task = cursor.fetchone()

            if not task:
                print("Task not found!")
                return

            # Regular users can update only their own tasks
            if user["role"] != "admin":
                cursor.execute("""
                    SELECT 1 FROM tasks
                    WHERE task_id = ? AND created_by = ?
                """, (int(task_id), user["user_id"]))

                if not cursor.fetchone():
                    print("You cannot update this task!")
                    return

            print("\nLeave a field blank to keep its current value.")

            title = input(f"Title [{task[0]}]: ").strip()
            description = input(
                f"Description [{task[1] or ''}]: "
            ).strip()

            print("\nPriority: 1. Low  2. Medium  3. High")
            priority_choice = input("Choose priority: ").strip()

            priorities = {
                "1": "Low",
                "2": "Medium",
                "3": "High"
            }

            if priority_choice and priority_choice not in priorities:
                print("Invalid priority!")
                return

            priority = priorities.get(
                priority_choice, task[2]
            )

            due_date = input(
                f"Due date [{task[3] or ''}]: "
            ).strip()

            if due_date:
                from datetime import datetime

                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date! Use YYYY-MM-DD.")
                    return
            else:
                due_date = task[3]

            print("\nStatus:")
            print("1. Pending")
            print("2. In Progress")
            print("3. Completed")

            status_choice = input("Choose status: ").strip()

            statuses = {
                "1": "Pending",
                "2": "In Progress",
                "3": "Completed"
            }

            if status_choice and status_choice not in statuses:
                print("Invalid status!")
                return

            status = statuses.get(status_choice, task[4])

            cursor.execute("""
                UPDATE tasks
                SET title = ?,
                    description = ?,
                    priority = ?,
                    due_date = ?,
                    status = ?
                WHERE task_id = ?
            """, (
                title or task[0],
                description or task[1],
                priority,
                due_date,
                status,
                int(task_id)
            ))

        print("Task updated successfully!")

    except sqlite3.Error as error:
        print("Database error:", error)

def delete_task(user):
    print("\n===== DELETE TASK =====")

    task_id = input("Enter task ID: ").strip()

    if not task_id.isdigit() or int(task_id) <= 0:
        print("Invalid task ID!")
        return

    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            if user["role"] == "admin":
                cursor.execute("""
                    SELECT title FROM tasks WHERE task_id = ?
                """, (int(task_id),))
            else:
                cursor.execute("""
                    SELECT title FROM tasks
                    WHERE task_id = ? AND created_by = ?
                """, (int(task_id), user["user_id"]))

            task = cursor.fetchone()

            if not task:
                print("Task not found or you don't have permission!")
                return

            print(f"Task: {task[0]}")
            confirm = input(
                "Are you sure you want to delete it? (yes/no): "
            ).strip().lower()

            if confirm != "yes":
                print("Deletion cancelled.")
                return

            cursor.execute("""
                DELETE FROM tasks WHERE task_id = ?
            """, (int(task_id),))

        print("Task deleted successfully!")

    except sqlite3.Error as error:
        print("Database error:", error)

def assign_task(user):
    if user["role"] != "admin":
        print("Access denied! Only admins can assign tasks.")
        return

    print("\n===== ASSIGN TASK =====")

    task_id = input("Enter Task ID: ").strip()
    user_id = input("Enter User ID to assign the task to: ").strip()

    if not task_id.isdigit() or int(task_id) <= 0:
        print("Invalid Task ID!")
        return

    if not user_id.isdigit() or int(user_id) <= 0:
        print("Invalid User ID!")
        return

    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()

            # Check whether the task exists
            cursor.execute(
                "SELECT title FROM tasks WHERE task_id = ?",
                (int(task_id),)
            )
            task = cursor.fetchone()

            if not task:
                print("Task not found!")
                return

            # Check whether the user exists
            cursor.execute(
                "SELECT name FROM users WHERE user_id = ?",
                (int(user_id),)
            )
            user = cursor.fetchone()

            if not user:
                print("User not found!")
                return

            # Assign the task
            cursor.execute("""
                INSERT INTO task_assignments (task_id, user_id)
                VALUES (?, ?)
            """, (int(task_id), int(user_id)))

        print(f"Task '{task[0]}' assigned to {user[0]} successfully!")

    except sqlite3.IntegrityError:
        print("This task is already assigned to that user!")

    except sqlite3.Error as error:
        print("Database error:", error)


def unassign_task(user):
    if user["role"] != "admin":
        print("Access denied! Only admins can unassign tasks.")
        return

    try:
        task_id = input("Enter Task ID: ").strip()
        user_id = input("Enter User ID to unassign: ").strip()

        if (
                not task_id.isdigit()
                or not user_id.isdigit()
                or int(task_id) <= 0
                or int(user_id) <= 0
        ):
            print("Invalid input! IDs must be positive numbers.")
            return
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT title FROM tasks WHERE task_id = ?",
                (int(task_id),)
            )
            task = cursor.fetchone()

            if not task:
                print("Task not found!")
                return

            cursor.execute(
                "SELECT name FROM users WHERE user_id = ?",
                (int(user_id),)
            )
            target_user = cursor.fetchone()

            if not target_user:
                print("User not found!")
                return

            cursor.execute("""
                DELETE FROM task_assignments
                WHERE task_id = ? AND user_id = ?
            """, (int(task_id), int(user_id)))

            if cursor.rowcount > 0:
                print(
                    f"Task '{task[0]}' unassigned from "
                    f"{target_user[0]} successfully!"
                )
            else:
                print("This task is not assigned to that user.")

    except sqlite3.Error as error:
        print("Database error:", error)


def update_assigned_task_status(user):
    print("\n===== UPDATE ASSIGNED TASK STATUS =====")

    try:
        task_id = input("Enter Task ID: ").strip()

        if not task_id.isdigit() or int(task_id) <= 0:
            print("Invalid Task ID!")
            return

        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT t.title, t.status
                FROM tasks t
                JOIN task_assignments ta
                    ON t.task_id = ta.task_id
                WHERE t.task_id = ?
                  AND ta.user_id = ?
            """, (int(task_id), user["user_id"]))

            task = cursor.fetchone()

            if not task:
                print("Task not found or not assigned to you!")
                return

            print("Task:", task[0])
            print("Current status:", task[1])
            print("1. Pending")
            print("2. In Progress")
            print("3. Completed")

            choice = input("Choose new status: ").strip()

            statuses = {
                "1": "Pending",
                "2": "In Progress",
                "3": "Completed"
            }

            if choice not in statuses:
                print("Invalid choice!")
                return

            cursor.execute("""
                UPDATE tasks
                SET status = ?
                WHERE task_id = ?
            """, (statuses[choice], int(task_id)))

        print("Task status updated successfully!")

    except sqlite3.Error as error:
        print("Database error:", error)


