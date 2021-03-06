import logging
import unittest as _ut
from unittest.mock import patch

from . import mock_jsonify, mock_req

logger = logging.getLogger(__name__)

class TestUsersRoute(_ut.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_jsonify = mock_jsonify
        cls.mock_req = mock_req
    
    def setUp(self):
        self.users = [
            dict(zip(
                ["username", "password", "fName", "lName", "email"],
                ["stallylol", "123456", "Stally", "Duan", "user1@gmail.com"]
            )),
            dict(zip(
                ["username", "password", "fName", "lName", "email"],
                ["shiyugun", "abcdef", "Shiyu", "Gao", "user2@gmail.com"]
            )),
            dict(zip(
                ["username", "password", "fName", "lName", "email"],
                ["aspenrocks", "78910", "Aspen", "Forster", "user3@gmail.com"]
            ))
        ]

    def tearDown(self):
        self.__class__.mock_jsonify.reset_mock()
        self.__class__.mock_req.reset_mock()

    def testRegister(self):
        '''confirm that the correct user data is passed to user manager's addOne method
        '''
        self.mock_req.json = self.users[0]
        from app.UserManager import UserManager
        with patch.object(UserManager, 'addOne') as mock_add_one:
            from app.routes.users import register
            register()
            mock_add_one.assert_called_with(self.users[0])

    def testRegisterDuplicateUsername(self):
        '''confirm that when a duplicate username is present, the view function propagates the exception
        '''
        from app.errors.api_exceptions import DuplicateKey
        from app.UserManager import UserManager
        with patch.object(UserManager, 'addOne', side_effect=DuplicateKey("duplicate username")):
            with self.assertRaises(DuplicateKey):
                from app.routes.users import register
                register()

    def testRegisterEmptyEmail(self):
        '''confirm that when email is not provided, the view function propagates the exception
        '''
        from app.errors.api_exceptions import InvalidArgument
        from app.UserManager import UserManager
        with patch.object(UserManager, 'addOne', side_effect=InvalidArgument("empty email")):
            with self.assertRaises(InvalidArgument):
                from app.routes.users import register
                register()

    def testRegisterReturnSuccess(self):
        '''confirm that when the user is added successfully, the view function returns success
        '''
        from app.UserManager import UserManager
        with patch.object(UserManager, 'addOne', return_value=True):
            from app.routes.users import register
            register()
            self.mock_jsonify.assert_called_with({"data": {"success": True}})

    def testFindUser(self):
        '''confirm that the username is passed to user manager's getOne method
        '''
        username = self.users[1]["username"]
        password = self.users[1]["password"]
        self.mock_req.json = {"username": username}
        from app.UserManager import UserManager
        with patch.object(UserManager, 'getOne') as mock_get_one:
            from app.routes.users import findUser
            findUser()
            mock_get_one.assert_called_with(username)

    def testFindUserSuccess(self):
        '''confirm that when crendentials exist, the view function returns success and user data
        '''
        user_data = self.users[2]
        self.mock_req.json = {"username": user_data["username"]}
        from app.UserManager import UserManager
        with patch.object(UserManager, 'getOne', return_value=user_data):
            from app.routes.users import findUser
            findUser()
            self.mock_jsonify.assert_called_with({"data": {"success": True, "user": user_data}})

    def testFindNonExistentUser(self):
        '''confirm that when username does not exist, the view function returns failure
        '''
        from app.UserManager import UserManager
        with patch.object(UserManager, 'getOne', return_value=None):
            from app.routes.users import findUser
            findUser()
            self.mock_jsonify.assert_called_with({"data": {"success": False}})
