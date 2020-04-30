from .DBManager import DBManager


class CarManager(DBManager):
    FIELDS = ["car_id", "year", "car_model", "body_type", "num_seats", 
                "car_colour", "cost_hour", "latitude", "longitude"]
    TABLE_NAME = "Car"


    def getMany(self, filt: dict) -> list:
        # dummy values
        return [
            {'make': "Audi", "body_type": "Sedan", "colour": "white", "seats": 4, 
                "location": (37, 144), "cost_per_hour": 0.5}
        ]
    
    def updateOne(self, carId, car: dict) -> bool:
        return True

    def getOne(self, carId) -> dict:
        return {}

    def addOne(self, car: dict):
        # returns carId
        return 0             