from .BaseService import BaseService

class UserService(BaseService):

    def getAllUsers(self):
        '''get all users
        '''
        url = "/users/search"
        data = {}
        users = self.post(url, data)
        return users

    def findExistingUser(self, username):
        '''find a user with <username>, return user data or None if not exists
        '''
        url="/users/search"
        data = {'username': username }
        result = self.post(url, data)
    
        # (python ternary operator)
        return result['user'] if result['success'] == True else None

    def registerUser(self, inputData:dict):
        '''register a user
        '''
        url="/users/registerUser"
        data = inputData
        output = self.post(url, data)

        return True if output['success'] == True else False
