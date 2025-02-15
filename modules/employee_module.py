from DatabaseTypeEnum import DatabaseTypeEnum
from repository.employeeـrepository_mongodb import EmployeeRepositoryMongodb
from repository.employeeـrepository_postgres import EmployeeRepositoryPostgres


class EmployeeModule:

    def __init__(self, db_helper):
        self.db_helper = db_helper


    def add_employee(self, name, email, job_title):
        if self.db_helper.db_type == DatabaseTypeEnum.POSTGRESQL:
            employee_repo = EmployeeRepositoryPostgres(self.db_helper)
            employee_repo.add_employees(name, email, job_title)
            print("✅ Employee added to PostgreSQL database!")

        elif self.db_helper.db_type == DatabaseTypeEnum.MONGODB:
            employee_repo = EmployeeRepositoryMongodb(self.db_helper)
            employee_repo.add_employees(name, email, job_title)
            print("✅ Employee added to MongoDB database!")

        else:
            print("❌ Unsupported database type.")


    def get_all_employees(self):
        employee_repo = EmployeeRepositoryPostgres(self.db_helper) if self.db_helper.db_type == DatabaseTypeEnum.POSTGRESQL else EmployeeRepositoryMongodb(self.db_helper)
        return employee_repo.get_all_employees()

    def get_employee_by_id(self, employee_id):

        employee_repo = EmployeeRepositoryPostgres(
            self.db_helper) if self.db_helper.db_type == DatabaseTypeEnum.POSTGRESQL else EmployeeRepositoryMongodb(
            self.db_helper)

        employees_df = employee_repo.get_all_employees()
        employee_data = employees_df[employees_df['id'] == employee_id]

        if employee_data.empty:
            return None

        return employee_data.iloc[0]

    def get_employees_by_title(self, job_title):
        employee_repo = EmployeeRepositoryPostgres(
            self.db_helper) if self.db_helper.db_type == DatabaseTypeEnum.POSTGRESQL else EmployeeRepositoryMongodb(
            self.db_helper)

        employees_df = employee_repo.get_all_employees()
        filtered_df = employees_df[employees_df['job_title'].str.lower() == job_title.lower()]

        if filtered_df.empty:
            return []
        return filtered_df.to_dict(orient='records')
