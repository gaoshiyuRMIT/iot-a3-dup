from .BaseService import BaseService

class CarService(BaseService):
    def getAllAvailableCars(self):
        url = "/cars/search"
        params = {"status": "available"}
        cars = self.get(url, params)
        return cars