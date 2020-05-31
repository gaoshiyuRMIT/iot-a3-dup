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
        '''add a new user

        :param dict newVal: a dictionary with all the fields and values of a user
        :return: whether a row is inserted
        :rtype: bool
        '''
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
        # returns iff. one row is updated
        return row == 1

    def getOne(self, username: str) -> list:
        '''get a user by supplying username

        :param int username: username
        :return: the user data
        :rtype: dict
        '''
        return super().getOne(username)

    def getMany(self, filt: dict) -> list:
        '''get all users that satisfy the query condition

        :param dict filt: the query condition
        :return: a list of dictionaries, each representing a user
        :rtype: list
        '''
        return super().getMany(filt)

    def updateOne(self, username, newUserVal: dict) -> bool:
        '''provided username and new values, update a user

        :param int username: username
        :param dict newUserVal: a dictionary specifying the fields to update and the values to update them with
        :return: whether a row is updated successfully
        :rtype: bool
        '''
        return super().updateOne(username, newUserVal)

    def deleteOne(self, username: str) -> bool:
        '''delete a user given username
        '''
        return super().deleteOne(username)