from urllib.parse import quote
from .base_service import BaseService

class UserService(BaseService):
    def get_all_users(self):
        '''get all users
        '''
        url = "/users/search"
        data = {}
        users = self.post(url, data)
        return users
    
    def add_user(self, new_val: dict) -> bool:
        url = "/users/add"
        data = self.post(url, new_val)
        return data["success"]

    def delete_user(self, username: str) -> bool:
        url = f"/users/{quote(username)}"
        data = self.delete(url)
        return data['success']

    def update_user(self, username: str, new_val: dict) -> bool:
        url = f"/users/{quote(username)}"
        data = self.put(url, new_val)
        return data["success"]

    def get_activity_types(self):
        url = f"/users/activity/types"
        return self.get(url, {})

    def find_user(self, username):
        '''establish whether user with <username>, return all user data or None 
        if username does not exist
        '''
        url = f"/users/{quote(username)}"
        data = self.get(url)
        return data