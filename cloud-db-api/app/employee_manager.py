from .DBManager import DBManager

class EmployeeManager(DBManager):
    FIELDS = ["username", "password", "fName", "lName", "email"]
    PK = "username"
    TABLE_NAME = "Employee"

    def getOne(self, username: str) -> dict:
        return super().getOne(username)

    def getMany(self, query: dict) -> list:
        return super().getMany(query)
    
    def updateOne(self, username: str, new_val: dict) -> bool:
        raise NotImplementedError

    def deleteOne(self, username: str) -> bool:
        raise NotImplementedError

    def addOne(self, new_val: dict) -> bool:
        raise NotImplementedError