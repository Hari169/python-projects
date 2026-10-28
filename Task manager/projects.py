import sqlite3

DATABASE_NAME = "task_management.db"


def create_project(user):
    if user["role"] != "admin":
        print("Access denied! Only admins can create projects.")
        return

    print("\n===== CREATE PROJECT =====")

    project_name = input("Enter project name: ").strip()
    description = input("Enter project description: ").strip()

    if not project_name:
        print("Project name cannot be empty!")
        return

    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO projects (project_name, description, created_by)
                VALUES (?, ?, ?)
            """, (project_name, description, user["user_id"]))

        print("Project created successfully!")

    except sqlite3.Error as error:
        print("Database error:", error)


def view_projects():
    print("\n===== ALL PROJECTS =====")

    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT p.project_id, p.project_name, p.description,
                       u.name, p.created_at
                FROM projects p
                LEFT JOIN users u ON p.created_by = u.user_id
                ORDER BY p.project_id
            """)

            projects = cursor.fetchall()

        if not projects:
            print("No projects found.")
            return

        for project in projects:
            print("-" * 40)
            print("Project ID:", project[0])
            print("Name:", project[1])
            print("Description:", project[2] or "No description")
            print("Created by:", project[3] or "Unknown")
            print("Created at:", project[4])

    except sqlite3.Error as error:
        print("Database error:", error)


def update_project(user):
    if user["role"] != "admin":
        print("Access denied! Only admins can update projects.")
        return

    print("\n===== UPDATE PROJECT =====")

    project_id = input("Enter Project ID: ").strip()

    if not project_id.isdigit() or int(project_id) <= 0:
        print("Invalid Project ID!")
        return

    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT project_name, description FROM projects WHERE project_id = ?",
                (int(project_id),)
            )
            project = cursor.fetchone()

            if not project:
                print("Project not found!")
                return

            print("Current name:", project[0])
            print("Current description:", project[1] or "None")
            print("Leave a field blank to keep its current value.")

            new_name = input("Enter new project name: ").strip()
            new_description = input("Enter new description: ").strip()

            new_name = new_name or project[0]
            new_description = new_description or project[1]

            cursor.execute("""
                UPDATE projects
                SET project_name = ?, description = ?
                WHERE project_id = ?
            """, (new_name, new_description, int(project_id)))

        print("Project updated successfully!")

    except sqlite3.Error as error:
        print("Database error:", error)



def delete_project(user):
    if user["role"] != "admin":
        print("Access denied! Only admins can delete projects.")
        return

    print("\n===== DELETE PROJECT =====")

    project_id = input("Enter Project ID: ").strip()

    if not project_id.isdigit() or int(project_id) <= 0:
        print("Invalid Project ID!")
        return

    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT project_name FROM projects WHERE project_id = ?",
                (int(project_id),)
            )
            project = cursor.fetchone()

            if not project:
                print("Project not found!")
                return

            print("Project:", project[0])
            confirm = input("Are you sure you want to delete it? (yes/no): ")

            if confirm.strip().lower() != "yes":
                print("Deletion cancelled.")
                return

            cursor.execute(
                "DELETE FROM projects WHERE project_id = ?",
                (int(project_id),)
            )

        print("Project deleted successfully!")

    except sqlite3.Error as error:
        print("Database error:", error)



