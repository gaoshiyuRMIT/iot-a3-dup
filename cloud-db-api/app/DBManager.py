import pymysql
from abc import ABC, ABCMeta, abstractmethod
from .db import getConn
from .errors.api_exceptions import InvalidArgument

class DBManager(ABC):
    FIELDS = []
    TYPES = []
    TABLE_NAME = ""

    @property
    def conn(self):
        return getConn()

    def getCursor(self, conn):
        return conn.cursor(pymysql.cursors.DictCursor)    

    @classmethod
    def keepValidFieldsOnly(cls, d: dict, throw=False) -> dict:
        if throw:
            invalidKeys = set(d.keys()) - set(cls.FIELDS)
            if len(invalidKeys) > 0:
                message = "invalid key(s): {}".format(", ".join(invalidKeys))
                raise InvalidArgument(message)
        return {k: d.get(k) for k in cls.FIELDS}

    @abstractmethod
    def getMany(self, filt: dict) -> list:
        # default implementation
        sql = f"select * from {self.TABLE_NAME}"
        if len(filt) > 0:
            sql += " where "
        condSql = []
        vals = []
        for k,v in filt.items():
            if isinstance(v, list) and len(v) == 2:
                if v[0] and v[1]:
                    s = "{} between %s and %s".format(k)
                    condSql.append(s)
                    vals.append(v[0])
                    vals.append(v[1])
                elif not v[0]:
                    s = "{} <= %s".format(k)
                    condSql.append(s)
                    vals.append(v[1])
                elif not v[1]:
                    s = "{} >= %s".format(k)
                    condSql.append(s)
                    vals.append(v[0])
            else:
                s = "{} = %s".format(k)
                condSql.append(s)
                vals.append(v)
        sql += " and ".join(condSql)
        res = []
        conn = self.conn
        try:
            with self.getCursor(conn) as cur:
                print("* generated sql: {}".format(cur.mogrify(sql, vals)))
                cur.execute(sql, vals)
                res = cur.fetchall()
        except Exception as e:
            conn.rollback()
            raise e
        return res

    @abstractmethod
    def getOne(self, id) -> dict:
        raise NotImplementedError

    @abstractmethod
    def updateOne(self, id, newVal: dict) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def addOne(self, newVal: dict) -> bool:
        raise NotImplementedError

