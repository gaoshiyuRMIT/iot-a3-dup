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
        '''get all cars that satisfy the query condition

        :param dict filt: the query condition
        :return: a list of dictionaries, each representing a car
        :rtype: list
        '''
        return super().getMany(filt)
    
    def updateOne(self, car_id, car: dict) -> bool:
        '''provided car_id and new values, update a car

        :param int car_id: car ID
        :param dict car: a dictionary specifying the fields to update and the values to update them with
        :return: whether a row is updated successfully
        :rtype: bool
        '''
        return super().updateOne(car_id, car)

    def getOne(self, carId) -> dict:
        '''get a car by supplying car_id

        :param int car_id: car ID
        :return: the car data
        :rtype: dict
        '''
        return super().getOne(carId)

    def addOne(self, car: dict):
        '''add a new car

        :param dict car: with all the fields and values of a car, except car_id
        :return: the auto-generated car_id
        :rtype: int
        '''
        car_id = super().addOne(car)
        return car_id

    def deleteOne(self, car_id: int) -> bool:
        '''delete a car, given car_id
        '''
        return super().deleteOne(car_id)