from tasks import (
    create_task,
    update_task,
    delete_task,
    assign_task,
    unassign_task,
    update_assigned_task_status
)
import sqlite3
DATABASE_NAME = "task_management.db"


def admin_dashboard(user):
    while True:
        print("\n===== ADMIN DASHBOARD =====")
        print("1. View All Users")
        print("2. View All Tasks")
        print("3. Create Task")
        print("4. Update Task")
        print("5. Delete Task")
        print("6. Assign Task")
        print("7. Unassign Task")
        print("8. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            try:
                with sqlite3.connect(DATABASE_NAME) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT user_id, name, email, role
                        FROM users
                    """)
                    users = cursor.fetchall()

                for item in users:
                    print(item)

            except sqlite3.Error as error:
                print("Database error:", error)

        elif choice == "2":
            try:
                with sqlite3.connect(DATABASE_NAME) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT task_id, title, status, priority, due_date
                        FROM tasks
                    """)
                    tasks = cursor.fetchall()

                if tasks:
                    for task in tasks:
                        print(task)
                else:
                    print("No tasks found.")

            except sqlite3.Error as error:
                print("Database error:", error)

        elif choice == "3":
            create_task(user)

        elif choice == "4":
            update_task(user)

        elif choice == "5":
            delete_task(user)


        elif choice == "6":

            assign_task(user)

        elif choice == "7":
            unassign_task(user)

        elif choice == "8":

            print("Logging out...")

            break

def user_dashboard(user):
    while True:
        print("\n===== USER DASHBOARD =====")
        print("1. View My Tasks")
        print("2. Create Task")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Update Assigned Task Status")
        print("6. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            try:
                with sqlite3.connect(DATABASE_NAME) as conn:
                    cursor = conn.cursor()

                    cursor.execute("""
                        SELECT DISTINCT
                            t.task_id,
                            t.title,
                            t.status,
                            t.priority,
                            t.due_date
                        FROM tasks AS t
                        LEFT JOIN task_assignments AS ta
                            ON t.task_id = ta.task_id
                        WHERE t.created_by = ?
                           OR ta.user_id = ?
                        ORDER BY t.task_id
                    """, (user["user_id"], user["user_id"]))

                    tasks = cursor.fetchall()

                if tasks:
                    print("\n===== MY TASKS =====")

                    for task in tasks:
                        print("-" * 35)
                        print(f"Task ID: {task[0]}")
                        print(f"Title: {task[1]}")
                        print(f"Status: {task[2]}")
                        print(f"Priority: {task[3]}")
                        print(f"Due Date: {task[4] or 'Not set'}")

                    print("-" * 35)

                else:
                    print("No tasks created or assigned to you.")

            except sqlite3.Error as error:
                print("Database error:", error)

        elif choice == "2":
            create_task(user)

        elif choice == "3":
            update_task(user)

        elif choice == "4":
            delete_task(user)

        elif choice == "5":
            update_assigned_task_status(user)

        elif choice == "6":
            print("Logging out...")
            break

        else:
            print("Invalid choice! Please try again.")

