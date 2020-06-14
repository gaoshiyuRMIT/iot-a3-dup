import unittest as _ut
from unittest.mock import MagicMock, patch
from . import mock_app

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
        self.activities = [
            {"activity": "login", "count": 34},
            {"activity": "add_booking", "count": 9},
            {"activity": "search_car", "count": 25}
        ]

    def test_get_all_users(self):
        '''confirm that all users are returned when status code is 200
        '''
        from app.services.user_service import UserService
        with patch.object(UserService, "post", return_value=self.users):
            result = UserService().get_all_users()
            self.assertEqual(self.users, result)
            
    def test_add_user(self):
        '''confirm that success is propagated when status is 200
        '''
        from app.services.user_service import UserService
        new_user = self.users[0]
        new_user['username'] = "test_add_user"
        with patch.object(UserService, "post", return_value={"success": True}):
            result = UserService().add_user(new_user)
            self.assertTrue(result)

    def test_delete_user(self):
        '''confirm that correct user is deleted & success is propagated when status is 200
        '''
        from app.services.user_service import UserService
        with patch.object(UserService, "delete", return_value={"success": True}) as mock_del:
            result = UserService().delete_user("shiyugun")
            self.assertTrue(result)
            mock_del.assert_called_with("/users/shiyugun")

    def test_update_user(self):
        '''confirm that updated values are passed to the right endpoint & success is propagated when status is 200
        '''
        from app.services.user_service import UserService
        new_user_val = self.users[0]
        new_user_val.pop("username")
        with patch.object(UserService, "put", return_value={"success": True}) as mock_put:
            result = UserService().update_user("shiyugun", new_user_val)
            self.assertTrue(result)
            mock_put.assert_called_with("/users/shiyugun/update", new_user_val)

    def test_get_activity_types(self):
        '''confirm that activity types & counts are returned
        '''
        from app.services.user_service import UserService
        with patch.object(UserService, "get", return_value=self.activities):
            result = UserService().get_activity_types()
            self.assertEqual(self.activities, result)

    def test_search_users(self):
        '''confirm that search result is returned when status is 200
        '''
        from app.services.user_service import UserService
        with patch.object(UserService, "post", return_value=self.users[:1]):
            result = UserService().search_users({"fName": "Stally"})    
            self.assertEqual(self.users[:1], result)

    def test_find_existing_user(self):
        '''confirm that username is passed to the right endpoint & user info is returned when status is 200
        '''
        from app.services.user_service import UserService
        with patch.object(UserService, "post", return_value=self.users[:1]):
            result = UserService().findExistingUser("Stally")
            self.assertEqual(self.users[0], result)