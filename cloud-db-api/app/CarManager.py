import pymysql as _p
from .DBManager import DBManager
from app import app
import logging
import pymysql as p
import json

from decimal import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

class CarManager(DBManager):
    FIELDS = ["car_id", "year", "car_model", "body_type", "num_seats", 
                "car_colour", "cost_hour", "latitude", "longitude", "car_status"]
    TABLE_NAME = "Car"

    def getMany(self, filt: dict) -> list:
        return super().getMany(filt)
    
    def updateOne(self, car_id, car: dict) -> bool:
        sql = f"update {self.TABLE_NAME} set "
        sqlAssg = []
        vals = []
        for k,v in car.items():
            sqlAssg.append(f"{k} = %s")
            vals.append(v)
        sql += ", ".join(sqlAssg)
        sql += " where car_id = %s"
        vals.append(car_id)
        conn = self.conn
        row = -1
        try:
            with conn.cursor() as cur:
                logger.debug("generated sql {}".format(cur.mogrify(sql, vals)))
                row = cur.execute(sql, vals)
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.exception("updating one car failed")
            raise
        return row == 1


    def getOne(self, carId) -> dict:
        sql = "SELECT * FROM " + self.TABLE_NAME + " WHERE car_id = %s"
        car = None
        conn = self.conn
        try:
            with self.getCursor(conn) as cursor:
                cursor.execute(sql, (carId,))
                car = cursor.fetchone()
        except (_p.OperationalError, _p.InternalError, _p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            raise
        except _p.ProgrammingError:
            #error rrelated to sql syntax etc
            raise
        except:
            raise
        return car
        

    def addOne(self, car: dict):
        sql = "insert into car ("
        keys = []
        vals = []
        for k,v in car.items():
            keys.append(k)
            vals.append(v)
        sql += ", ".join(keys) + ") values ("
        sql += ", ".join(["%s"] * len(keys)) + ")"
        conn = self.conn
        car_id = -1
        try:
            with conn.cursor() as cur:
                logger.debug("generated sql: {}".format(cur.mogrify(sql, vals)))
                cur.execute(sql, vals)
                conn.commit()
                cur.execute("select last_insert_id()")
                car_id = cur.fetchone()[0]
        except Exception as e:
            conn.rollback()
            logger.exception("inserting one car failed")
            raise
        # returns carId
        return car_id      