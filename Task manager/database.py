import sqlite3

DATABASE_NAME = "task_management.db"


def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")

    # 1. Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
            CHECK (role IN ('admin', 'user'))
    )
    """)

    # 2. Projects table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT NOT NULL,
        description TEXT,
        created_by INTEGER NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by)
            REFERENCES users(user_id)
    )
    """)

    # 3. Categories table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE NOT NULL
    )
    """)

    # 4. Tasks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL DEFAULT 'Pending'
            CHECK (status IN ('Pending', 'In Progress', 'Completed')),
        priority TEXT NOT NULL DEFAULT 'Medium'
            CHECK (priority IN ('Low', 'Medium', 'High')),
        due_date TEXT,
        created_by INTEGER NOT NULL,
        project_id INTEGER,
        category_id INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (created_by)
            REFERENCES users(user_id),

        FOREIGN KEY (project_id)
            REFERENCES projects(project_id)
            ON DELETE SET NULL,

        FOREIGN KEY (category_id)
            REFERENCES categories(category_id)
            ON DELETE SET NULL
    )
    """)

    # 5. Task assignments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS task_assignments (
        assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        assigned_at TEXT DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (task_id)
            REFERENCES tasks(task_id)
            ON DELETE CASCADE,

        FOREIGN KEY (user_id)
            REFERENCES users(user_id)
            ON DELETE CASCADE,

        UNIQUE (task_id, user_id)
    )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")
    print("All five tables are ready.")


if __name__ == "__main__":
    create_database()