from .BaseService import BaseService

class UserService(BaseService):

    def getAllUsers(self):
        url = "/users/search"
        data = {}
        users = self.post(url, data)
        return users

    def isValidUser(self, username, password):
        url ="/users/login"
        data = {'username':username, 'password':password}
        user = self.post(url, data)

        # (python ternary operator)
        return True if user['success'] == True else False
