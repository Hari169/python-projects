import sqlite3
import hashlib
import os

DATABASE_NAME = "task_management.db"


def hash_password(password):
    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600000
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password, stored_hash):
    try:
        salt_hex, hash_hex = stored_hash.split(":")
        salt = bytes.fromhex(salt_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            600000
        )

        return password_hash.hex() == hash_hex

    except (ValueError, TypeError):
        return False


def register():
    print("\n===== USER REGISTRATION =====")

    name = input("Enter your name: ").strip()
    email = input("Enter your email: ").strip().lower()
    password = input("Enter your password: ")

    if not name or not email or not password:
        print("Error: All fields are required!")
        return

    if "@" not in email or "." not in email.split("@")[-1]:
        print("Error: Enter a valid email address!")
        return

    if len(password) < 8:
        print("Error: Password must contain at least 8 characters!")
        return

    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]

            # First registered user becomes admin
            role = "admin" if user_count == 0 else "user"

            password_hash = hash_password(password)

            cursor.execute("""
                INSERT INTO users (name, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            """, (name, email, password_hash, role))

        print(f"Registration successful! Your role is: {role}")

    except sqlite3.IntegrityError:
        print("Error: This email is already registered!")

    except sqlite3.Error as error:
        print("Database error:", error)

def login():
    print("\n===== USER LOGIN =====")

    name = input("Enter your name: ").strip()
    password = input("Enter your password: ")

    if not name or not password:
        print("Error: Name and password are required!")
        return None

    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT user_id, name, password_hash, role
                FROM users
                WHERE name = ? COLLATE NOCASE
            """, (name,))

            user = cursor.fetchone()

        if user and verify_password(password, user[2]):
            print(f"\nWelcome, {user[1]}!")
            print(f"Role: {user[3]}")

            return {
                "user_id": user[0],
                "name": user[1],
                "role": user[3]
            }

        print("Invalid name or password!")
        return None

    except sqlite3.Error as error:
        print("Database error:", error)
        return None
if __name__ == "__main__":
    login()