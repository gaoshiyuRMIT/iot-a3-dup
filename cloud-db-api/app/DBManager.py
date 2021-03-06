import logging
import pymysql
from abc import ABC, ABCMeta, abstractmethod
from .db import getConn
from .errors.api_exceptions import InvalidArgument

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DBManager(ABC):
    FIELDS = []
    TABLE_NAME = ""
    PK = ""

    @property
    def conn(self):
        '''get db connection
        '''
        return getConn()

    def getCursor(self, conn):
        '''create a cursor that returns dictionaries instead of lists

        :param pymysql.Connection conn: db connection
        :return: a cursor that returns dictionaries
        '''
        return conn.cursor(pymysql.cursors.DictCursor)    

    @classmethod
    def keepValidFieldsOnly(cls, d: dict, throw=False) -> dict:
        '''provided a dictionary, remove fields that does not belong to this entity (see subclass),
        and fill in empty fields with None

        :param dict d: a dictionary representing an entity instance or a filter
        :param bool throw: whether to throw an error if a field is found to not belong to this entity
        '''
        d = d or {}
        if throw:
            invalidKeys = set(d.keys()) - set(cls.FIELDS)
            if len(invalidKeys) > 0:
                message = "invalid key(s): {}".format(", ".join(invalidKeys))
                raise InvalidArgument(message)
        return {k: d.get(k) for k in cls.FIELDS}


    @abstractmethod
    def getMany(self, filt: dict) -> list:
        '''get all the records that satisfy the query condition specified in a dictionary

        :param dict filt: a query condition dictionary, specifying either the exact value or the range of certain fields
        :return: entities (see subclasses) that match this query
        :rtype: list
        '''
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
    def getOne(self, id) -> list:
        '''provided the primary key value, get one entity instance

        :param (any) id: value of id or primary key
        :return: one record which has this id
        :rtype: dict
        '''
        sql = f"select * from {self.TABLE_NAME} where {self.PK} = %s"
        vals = [id]
        one = None
        conn = self.conn
        try:
            with self.getCursor(conn) as cur:
                cur.execute(sql, vals)
                one = cur.fetchone()
        except:
            logger.exception("getting one item by id failed")
            raise
        return one

    @abstractmethod
    def deleteOne(self, id) -> bool:
        '''delete one instance of this entity, provided the value of primary key is given

        :param (any) id: value of primary key
        :return: whether a row is deleted successfully
        :rtype: bool
        '''
        sql = f"delete from {self.TABLE_NAME} where {self.PK} = %s"
        vals = [id]
        row = -1
        conn = self.conn
        try:
            with conn.cursor() as cur:
                row = cur.execute(sql, vals)
            conn.commit()
        except:
            conn.rollback()
            logger.exception("deleting one instance failed")
            raise
        return row == 1

    @abstractmethod
    def updateOne(self, id, newVal: dict) -> bool:
        '''provided id and new values to update, update one record 

        :param (any) id: value of primary key
        :param dict newVal: a dictionary specifying the new values for certain fields
        :return: whether a row is updated successfully
        :rtype: bool
        '''
        sql = f"update {self.TABLE_NAME} set "
        sqlAssg = []
        vals = []
        for k,v in newVal.items():
            sqlAssg.append(f"{k} = %s")
            vals.append(v)
        sql += ", ".join(sqlAssg)
        sql += f" where {self.PK} = %s"
        vals.append(id)
        conn = self.conn
        row = -1
        try:
            with conn.cursor() as cur:
                logger.debug("generated sql {}".format(cur.mogrify(sql, vals)))
                row = cur.execute(sql, vals)
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.exception("updating one item failed")
            raise
        return row == 1

    
    @abstractmethod
    def addOne(self, newVal: dict):
        '''default implementation

        :param dict newVal: a dictionary, its key being the column name and its value being the value of that column
        :returns: id generated by mysql auto-incrementing
        :rtype: int
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
        id_ = None
        try:
            with conn.cursor() as cur:
                logger.debug("generated sql: {}".format(cur.mogrify(sql, vals)))
                cur.execute(sql, vals)
                conn.commit()
                cur.execute("select last_insert_id()")
                id_ = cur.fetchone()[0]
        except Exception as e:
            conn.rollback()
            logger.exception("inserting one item failed")
            raise
        # returns primary key
        return id_
