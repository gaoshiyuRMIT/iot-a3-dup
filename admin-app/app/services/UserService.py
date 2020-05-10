from .BaseService import BaseService

class UserService(BaseService):

    def getAllUsers(self):
        url = "/users/search"
        data = {}
        users = self.post(url, data)
        return users

    def isValidUser(self, username, password) -> bool:
        url ="/users/login"
        data = {'username':username, 'password':password}
        user = self.post(url, data)

        # (python ternary operator)
        return True if user['success'] == True else False

    def getValidUser(self, username, password):
        url ="/users/login"
        data = {'username':username, 'password':password}
        user = self.post(url, data)

        # (python ternary operator)
        return user['fname'] if user['success'] == True else None
