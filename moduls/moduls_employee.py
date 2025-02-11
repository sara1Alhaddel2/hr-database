
class Employee:
    employee_repo = None

    def __init__(self, employee_data):

        self.id = employee_data.get('id')
        self.name = employee_data.get('name')
        self.email = employee_data.get('email')
        self.job_title = employee_data.get('job_title')

    @classmethod
    def set_repository(cls, employee_repo):
        cls.employee_repo = employee_repo

    @classmethod
    def add_employee(cls, name, email, job_title):
        cls.employee_repo.add_employee(name, email, job_title)

    @classmethod
    def get_all_employees(cls):
        return cls.employee_repo.get_all_employees()

    @classmethod
    def get_employee_by_id(cls, employee_id):
        employees_df = cls.employee_repo.get_all_employees()

        employee_data = employees_df[employees_df['id'] == employee_id]

        if employee_data.empty:
            return None

        row = employee_data.iloc[0]
        return cls(row.to_dict())
    @classmethod
    def get_employees_by_title(cls, job_title):
        employees_df = cls.employee_repo.get_all_employees()

        filtered_df = employees_df[employees_df['job_title'].str.lower() == job_title.lower()]

        if filtered_df.empty:
            return []

        return [cls(row.to_dict()) for _, row in filtered_df.iterrows()]
