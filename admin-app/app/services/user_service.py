from urllib.parse import quote
from .base_service import BaseService

class UserService(BaseService):
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
