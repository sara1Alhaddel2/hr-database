import self

from DatabaseTypeEnum import DatabaseTypeEnum
from utils.database_config import DatabaseHelper
from modules.employee_module import EmployeeModule

# Initialize the DatabaseHelper
db_helper = DatabaseHelper()
employee_module = EmployeeModule(db_helper)

# Check if the connection is valid before starting the program
def check_database_connection():
    try:
        if db_helper.db_type == DatabaseTypeEnum.MONGODB:
            # Check MongoDB connection
            if db_helper.client is None:
                raise Exception("❌ MongoDB client is not connected.")
        elif db_helper.db_type == DatabaseTypeEnum.POSTGRESQL:
            # Check PostgreSQL connection
            if db_helper.connection is None:
                raise Exception("❌ PostgreSQL connection is not established.")
        else:
            raise Exception(f"❌ Unsupported database type: {db_helper.db_type}.")
        print(f"✅ Successfully connected to {db_helper.db_type.value} database.")
    except Exception as e:
        print(str(e))
        exit(1)  # Exit if database connection fails



def main():
    # Before running the program, check the database connection
    check_database_connection()

    print("🚀 Running Employee Management System")

    while True:
        print("\nMain Menu:")
        print("1. Manage Employees")
        print("2. Exit")
        choice = input("Enter your choice (1-2): ")

        if choice == '1':
            employee_menu()
        elif choice == "2":
            print("Exiting the program.")
            db_helper.close()  # Assuming `close` is a method that closes connections
            break
        else:
            print("Invalid choice, please try again.")

def employee_menu():
    while True:
        print("\nEmployee Menu:")
        print("1. Add Employee")
        print("2. List All Employees")
        print("3. Get Employee by ID")
        print("4. Get Employees by Job Title")
        print("5. Back to Main Menu")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            name = input("Enter employee's name: ").strip()
            email = input("Enter employee's email: ").strip()
            job_title = input("Enter employee's job title: ").strip()
            employee_module.add_employee(name, email, job_title)
            print("✅ Employee added successfully!")

        elif choice == '2':
            employees = employee_module.get_all_employees()
            if employees.empty:
                print("⚠️ No employees found.")
            else:
                print("\n📋 Employee List:")
                print(employees.to_string(index=False))

        elif choice == '3':
            employee_id = input("Enter Employee ID to search: ").strip()
            if not employee_id.isdigit():
                print("⚠️ Invalid Employee ID! Please enter a valid number.")
                continue

            employee = employee_module.get_employee_by_id(int(employee_id))
            if employee is not None:  # Check if the employee is found
                print("\n👤 Employee Details:")
                # Print details in a clear format
                print(f"🔹 ID: {employee['id']}")
                print(f"🔹 Name: {employee['name']}")
                print(f"🔹 Email: {employee['email']}")
                print(f"🔹 Job Title: {employee['job_title']}")
            else:
                print("⚠️ Employee not found.")



        elif choice == '4':
            job_title = input("Enter job title to search: ").strip()
            employees = employee_module.get_employees_by_title(job_title)

            if not employees:
                print(f"⚠️ No employees found with job title '{job_title}'.")

            else:
                print(f"\n📋 Employees with job title '{job_title}':")
                for emp in employees:
                    print(f"\n🔹 ID: {emp['id']}")
                    print(f"🔹 Name: {emp['name']}")
                    print(f"🔹 Email: {emp['email']}")
                    print(f"🔹 Job Title: {emp['job_title']}")
                    print("-" * 30)  # Fancier separation between employees


        elif choice == '5':
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
