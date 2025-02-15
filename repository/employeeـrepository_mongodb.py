import pandas as pd


class EmployeeRepositoryMongodb:
    def __init__(self, db_helper):
        self.db_helper = db_helper

    def add_employees(self, name, email, job_title):
        data = {"name": name, "email": email, "job_title": job_title}
        result = self.db_helper.execute_mongo_query("employees", "insert", data=data)
        if result:
            print("✅ Employee added successfully!")

    def get_all_employees(self):
        # استرجاع البيانات باستخدام الاستعلام "find"
        result = self.db_helper.execute_mongo_query("employees", "find")

        # إذا لم تكن النتيجة موجودة، نرجع DataFrame فارغة
        if not result:
            return pd.DataFrame()

        # تحويل النتيجة إلى DataFrame
        return pd.DataFrame(result, columns=['id', 'name', 'email', 'job_title'])