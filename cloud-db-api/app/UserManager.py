from .DBManager import DBManager

class UserManager(DBManager):
    FIELDS = ["username", "password", "fName", "lName", "email"]
    TABLE_NAME = "User"

    def addOne(self, newUser: dict) -> bool:
        return True

    def getOne(self, filt: dict) -> list:
        return super().getOne(filt)

    def getMany(self, filt: dict) -> list:
        return super().getMany(filt)

    def updateOne(self, userId, newUserVal: dict) -> bool:
        raise NotImplementedError