import unittest as _ut
from unittest.mock import MagicMock, patch
from . import mock_app

class TestEmployeeServices(_ut.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_app = mock_app

    def tearDown(self):
        self.__class__.mock_app.reset_mock()

    def setUp(self):
        keys = ('username', 'password', 'fName', 'lName', 'email', 'role')
        emp_values = [
            ["shiyu_admin", "$5$rounds=1000$xHvtszBgCAgnn4aq$yJHUxh78iVHeaRnGx09ucuAa3MrgaTwthHeJ7PaCOx.", "Shiyu", "Gao", "shiyu.gao1@staff.com", "admin"],
            ["shiyu_engineer", "$5$rounds=1000$xHvtszBgCAgnn4aq$yJHUxh78iVHeaRnGx09ucuAa3MrgaTwthHeJ7PaCOx.", "Shiyu", "Gao", "shiyu.gao2@staff.com", "engineer"],
            ["shiyu_manager", "$5$rounds=1000$xHvtszBgCAgnn4aq$yJHUxh78iVHeaRnGx09ucuAa3MrgaTwthHeJ7PaCOx.", "Shiyu", "Gao", "shiyu.gao3@staff.com", "manager"],
        ]
        self.employees = [dict(zip(keys, v)) for v in emp_values]

    def test_find_employee(self):
        '''confirm that correct username is passed to the get one employee endpoint and employee value is returned when status is 200
        '''
        from app.services.employee_service import EmployeeService
        with patch.object(EmployeeService, "get", return_value=self.employees[0]) as mock_get:
            result = EmployeeService().find_employee("shiyu_admin")
            self.assertEqual(self.employees[0], result)
            mock_get.assert_called_with("/employees/shiyu_admin")