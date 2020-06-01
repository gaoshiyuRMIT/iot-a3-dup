from urllib.parse import quote
from .base_service import BaseService

class EmployeeService(BaseService):
    def find_employee(self, username):
        url = f"/employees/{quote(username)}"
        data = self.get(url)
        return data