import logging
import unittest as _ut
from unittest.mock import MagicMock, patch
from unittests import RESTFUL_API_URL
from . import mock_app

logger = logging.getLogger(__name__)

class TestUserServices(_ut.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_app = mock_app

    def tearDown(self):
        self.__class__.mock_app.reset_mock()

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

    def test_get_all_users(self):
        '''confirm that all users are returned
        '''
        from app.services.UserService import UserService
        with patch.object(UserService, "post", return_value=self.users) as mock_post:
            users = UserService().getAllUsers()
            self.assertEqual(self.users, users)

    def test_find_existing_user_success(self):
        '''confirm that when successful, user data is returned
        '''
        from app.services.UserService import UserService
        with patch.object(UserService, "post", return_value={"success": True, "user": self.users[0]}) \
                as mock_post:
            user = UserService().findExistingUser("stallylol")
            self.assertEqual(self.users[0], user)
            mock_post.assert_called_with("/users/search", {"username": "stallylol"})

    def test_find_existing_user_failure(self):
        '''confirm that when failed, method returns None
        '''
        from app.services.UserService import UserService
        with patch.object(UserService, "post", return_value={"success": False}) \
                as mock_post:
            user = UserService().findExistingUser("stallylol_doesnt_exist")
            self.assertIsNone(user)
            mock_post.assert_called_with("/users/search", {"username": "stallylol_doesnt_exist"})
            
    def test_register_user(self):
        '''confirm that success is propagated
        '''
        from app.services.UserService import UserService
        with patch.object(UserService, "post", return_value={"success": True}) \
                as mock_post:
            success = UserService().registerUser(self.users[0])
            self.assertTrue(success)
            mock_post.assert_called_with("/users/registerUser", self.users[0])