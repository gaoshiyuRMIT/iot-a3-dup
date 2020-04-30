from .DBManager import DBManager

class UserManager(DBManager):
    FIELDS = ["username", "password", "fName", "lName", "email"]
    TABLE_NAME = "User"

    def addOne(self, newUser: dict) -> bool:
        return True

    def getOne(self, userId) -> dict:
        return {}

    def getMany(self, filt: dict) -> list:
        try:
            with self.conn.cursor() as cur:
                # dummy sql
                # formatted string literal: python3.6+
                cur.execute(f"select * from {self.TABLE_NAME}")
                return cur.fetchall()
        except Exception:
            self.conn.rollback()
            raise

    def updateOne(self, userId, newUserVal: dict) -> bool:
        raise NotImplementedError