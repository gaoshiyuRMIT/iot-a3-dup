from urllib.parse import quote
from .base_service import BaseService

class UserService(BaseService):
    def get_all_users(self):
        '''get all users

        :return: all users
        :rtype: list
        '''
        url = "/users/search"
        data = {}
        users = self.post(url, data)
        return users
    
    def add_user(self, new_val: dict) -> bool:
        '''add a new user

        :param dict new_val: key-value map representing a new user
        :return: whether the operation is successful
        :rtype: bool
        '''
        url = "/users/registerUser"
        data = self.post(url, new_val)
        return data["success"]

    def delete_user(self, username: str) -> bool:
        '''given username, delete a user

        :param str username: username of the user to delete
        :return: whether the deletion is successful
        :rtype: bool
        '''
        url = f"/users/{quote(username)}"
        data = self.delete(url)
        return data['success']

    def update_user(self, username: str, new_val: dict) -> bool:
        '''given username, update the user with new values

        :param str username: username of the user to update
        :param dict new_val: key-value map to update the user to be
        :return: whether the operation is successful
        :rtype: bool
        '''
        url = f"/users/{quote(username)}/update"
        data = self.put(url, new_val)
        return data["success"]

    def get_activity_types(self):
        '''get users' activity types & counts

        :return: users' activities and counts, each item looks like {"activity": "XX", "count": x}
        :rtype: list
        '''
        url = f"/users/activity/types"
        return self.get(url, {})
    
    def search_users(self, query: dict):
        '''search for users given a query dict

        :param dict query: key-value/range to match users with
        :return: all users that satisfy the query
        :rtype: list
        '''
        url = "/users/search"
        data = query
        cars = self.post(url, data)
        return cars
    
    def findExistingUser(self, username):
        '''establish whether user with <username>, return all user data or None if username does not exist
        
        :param str username: username to look for
        :return: user info
        :rtype: dict
        '''
        url="/users/search"
        data = {'username': username }
        result = self.post(url, data)
    
        return result[0] if len(result) > 0 else None