from .DBManager import DBManager


class CarManager(DBManager):
    FIELDS = ["make", 'body_type', "colour", "seats", "location_long", "location_lat", 
                "cost_per_hour", "status"]
    TABLE_NAME = "car"


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