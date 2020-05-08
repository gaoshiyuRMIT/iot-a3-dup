from .DBManager import DBManager
from app import app
from flask import logging
import pymysql as p
import json

from decimal import *

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

class CarManager(DBManager):
    FIELDS = ["car_id", "year", "car_model", "body_type", "num_seats", 
                "car_colour", "cost_hour", "latitude", "longitude", "status"]
    TABLE_NAME = "Car"

    def getMany(self, filt: dict) -> list:
        app.logger.info(json.dumps([("test", Decimal('3.5'), Decimal('4.3'))], cls=DecimalEncoder))

        app.logger.info(json.dumps(self.getAll(), cls=DecimalEncoder))
        return [{}]
    
    def updateOne(self, carId, car: dict) -> bool:
        return True

    def getOne(self, carId) -> dict:
        return {}

    def addOne(self, car: dict):
        # returns carId
        return 0            

    def printConn(self):
        return self.conn

    """getAll() returns all the records in the Car table as a
    set/tuple of tuples."""
    def getAll(self):
        sql = "SELECT * FROM " + self.TABLE_NAME
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                resultall = cursor.fetchall() #must be stored in a variable as the finally claues will execute prior to the return stattement
                return list(resultall)
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except:
            pass # unkown error type