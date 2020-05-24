from .BaseService import BaseService

class CarService(BaseService):
    def getAllAvailableCars(self):
        url = "/cars/search"
        data = {"car_status": "available"}
        cars = self.post(url, data)
        return cars

    def searchCars(self, filterD: dict) -> list:
        url = "/cars/search"
        cars = self.post(url, filterD)
        # for car in cars:
        #     latS, longS = CarService.transformLocation(car['latitude'], car['longitude'])
        #     car['latitude'], car['longitude'] = latS, longS
        return cars

    def getCar(self, car_id: int) -> dict:
        url = "/cars/{}".format(car_id)
        car = self.get(url)
        return car

    def updateCar(self, car_id:int, newCarVal):
        url = "/cars/{}/update".format(car_id)
        self.put(url, newCarVal)

    @staticmethod
    def transformLocation(lat, long_) -> tuple:
        if lat < 0:
            latS = "{} S".format(-lat)
        elif lat > 0:
            latS = "{} N".format(lat)
        if long_ < 0:
            longS = "{} W".format(-long_)
        elif long_ > 0:
            longS = "{} E".format(long_)
        return latS, longS