from .DBManager import DBManager

class UserManager(DBManager):
    FIELDS = ["username", "password", "firstName", "lastName", "email"]
    TABLE_NAME = "user"

    def addOne(self, newUser: dict) -> bool:
        return True

    def getOne(self, userId) -> dict:
        return {}

    def getMany(self, filt: dict) -> list:
        return []

    def updateOne(self, userId, newUserVal: dict) -> bool:
        raise NotImplementedError