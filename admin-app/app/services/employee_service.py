from urllib.parse import quote
from .base_service import BaseService

class EmployeeService(BaseService):
    def find_employee(self, username):
        '''find an emplyoee with <username>, return all employee data or None 
        if username does not exist
        '''
        url = f"/employees/{quote(username)}"
        data = self.get(url)
        return data
    
    def register_employee(self, data:dict):
        '''register a new employee 
        '''
        url=
        