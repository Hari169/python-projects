from dashboards import admin_dashboard, user_dashboard
import auth
from database import create_database


def main_menu():
    while True:
        print("\n===== TASK MANAGEMENT SYSTEM =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            auth.register()

        elif choice == "2":
            user = auth.login()

            if user:
                if user["role"] == "admin":
                    admin_dashboard(user)
                else:
                    user_dashboard(user)

        elif choice == "3":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    create_database()
    main_menu()