import pandas as pd

class EmployeeRepository:
    def __init__(self, db_helper):
        self.db_helper = db_helper

    def add_employee(self, name, email, job_title):
        query = "INSERT INTO employees (name, email, job_title) VALUES (%s, %s, %s)"
        self.db_helper.execute_query(query, (name, email, job_title))
        print("✅ Employee added successfully!")

    def get_all_employees(self):
        query = "SELECT id, name, email, job_title FROM employees"
        result = self.db_helper.execute_query(query, fetch=True)

        if not result:
            return pd.DataFrame()

        return pd.DataFrame(result, columns=['id', 'name', 'email', 'job_title'])
