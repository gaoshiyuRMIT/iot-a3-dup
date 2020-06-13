from urllib.parse import quote
from .base_service import BaseService

'''EmployeeService communicates with cloud-db-api, which communicates with database'''
class EmployeeService(BaseService):
    
    def find_employee(self, username):
        '''find an emplyoee with <username>, return all employee data or None if username does not exist
        
        :param str username: username of the employee
        :return: None if the employee does not exist, otherwise the found employee info
        :rtype: dict or None
        '''
        url = f"/employees/{quote(username)}"
        data = self.get(url)
        return data

