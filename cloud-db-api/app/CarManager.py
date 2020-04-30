from .DBManager import DBManager


class CarManager(DBManager):
    FIELDS = ["car_id", "year", "car_model", "body_type", "num_seats", 
                "car_colour", "cost_hour", "latitude", "longitude"]
    TABLE_NAME = "Car"


    def getMany(self, filt: dict) -> list:
        # dummy values
        return [
            {"car_id": 1, "year": 2015, 'car_model': "Audi S3", "body_type": "Sedan", 
                "car_colour": "white", "num_seats": 4, "latitude": 37, "longitude": 144, 
                "cost_hour": 0.5}
        ]
    
    def updateOne(self, carId, car: dict) -> bool:
        return True

    def getOne(self, carId) -> dict:
        return {}

    def addOne(self, car: dict):
        # returns carId
        return 0             