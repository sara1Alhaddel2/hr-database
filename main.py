from utils.database_config import DatabaseHelper
from repository.employee_repository import EmployeeRepository
from moduls.moduls_employee import Employee

db_helper = DatabaseHelper()

employee_repo = EmployeeRepository(db_helper)

Employee.set_repository(employee_repo)


def main():
    print("🚀 Running Employee Management System")

    while True:
        print("\nMain Menu:")
        print("1. Manage Employees")
        print("2. Exit")
        choice = input("Enter your choice (1-2): ")

        if choice == '1':
            employee_menu()
        elif choice == '2':
            print("Exiting the program.")
            db_helper.close()
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
            Employee.add_employee(name, email, job_title)
            print("✅ Employee added successfully!")

        elif choice == '2':
            employees = Employee.get_all_employees()
            if employees.empty:
                print("⚠️ No employees found.")
            else:
                print("\n📋 Employee List:")
                print(employees)

        elif choice == '3':
            employee_id = input("Enter Employee ID to search: ").strip()
            if not employee_id.isdigit():
                print("⚠️ Invalid Employee ID! Please enter a valid number.")
                continue

            employee = Employee.get_employee_by_id(int(employee_id))
            if employee:
                print("\n👤 Employee Details:")
                print(f"🔹 ID: {employee.id}")
                print(f"🔹 Name: {employee.name}")
                print(f"🔹 Email: {employee.email}")
                print(f"🔹 Job Title: {employee.job_title}")
            else:
                print("⚠️ Employee not found.")

        elif choice == '4':
            job_title = input("Enter job title to search: ").strip()
            employees = Employee.get_employees_by_title(job_title)

            if not employees:
                print(f"⚠️ No employees found with job title '{job_title}'.")
            else:
                print("\n📋 Employees with this job title:")
                for emp in employees:
                    print(f"🔹 ID: {emp.id}, Name: {emp.name}, Email: {emp.email}, Job Title: {emp.job_title}")

        elif choice == '5':
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
