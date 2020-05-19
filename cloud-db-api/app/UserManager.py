import logging
import pymysql
from .DBManager import DBManager
from app.errors.api_exceptions import DuplicateKey, InvalidArgument

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class UserManager(DBManager):
    FIELDS = ["username", "password", "fName", "lName", "email"]
    TABLE_NAME = "User"
    PK = "username"

    def addOne(self, newVal: dict):
        sql = f"insert into {self.TABLE_NAME} ("
        keys = []
        vals = []
        for k,v in newVal.items():
            keys.append(k)
            vals.append(v)
        sql += ", ".join(keys) + ") values ("
        sql += ", ".join(["%s"] * len(keys)) + ")"
        conn = self.conn
        row = -1
        try:
            with conn.cursor() as cur:
                logger.debug("generated sql: {}".format(cur.mogrify(sql, vals)))
                row = cur.execute(sql, vals)
                conn.commit()
        except pymysql.err.IntegrityError as e:
            conn.rollback()
            msg = str(e).lower()
            if "duplicate" in msg and "key" in msg:
                raise DuplicateKey(f"failed adding a user with duplicate username: `{newVal['username']}`")
            if "cannot be null" in msg:
                raise InvalidArgument(f"failed adding a user with invalid email: `{newVal['email']}`")
            raise
        except Exception as e:
            conn.rollback()
            logger.exception("inserting one user failed")
            raise
        # returns primary key
        return row == 1

    def getOne(self, username: str) -> list:
        return super().getOne(username)

    def getMany(self, filt: dict) -> list:
        return super().getMany(filt)

    def updateOne(self, username, newUserVal: dict) -> bool:
        return super().updateOne(username, newUserVal)