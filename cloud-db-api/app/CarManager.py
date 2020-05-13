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
    PK = "car_id"

    def getMany(self, filt: dict) -> list:
        return super().getMany(filt)
    
    def updateOne(self, car_id, car: dict) -> bool:
        return super().updateOne(car_id, car)

    def getOne(self, carId) -> dict:
        return super().getOne(carId)

    def addOne(self, car: dict):
        car_id = super().addOne(car)
        return car_id