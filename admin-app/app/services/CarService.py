from .BaseService import BaseService

class CarService(BaseService):
    def getAllAvailableCars(self):
        '''get all available cars

        :return: all available cars
        :rtype: list
        '''
        url = "/cars/search"
        data = {"car_status": "available"}
        cars = self.post(url, data)
        return cars

    def searchCars(self, filterD: dict) -> list:
        '''search for cars, providing a filter dictionary

        :param dict filterD: filter dictionary, specifying the exact value / range of a car's fields
        :return: a list of cars - search result
        :rtype: list
        '''
        url = "/cars/search"
        cars = self.post(url, filterD)
        for car in cars:
            latS, longS = CarService.transformLocation(car['latitude'], car['longitude'])
            car['latitude'], car['longitude'] = latS, longS
        return cars

    def getCar(self, car_id: int) -> dict:
        '''get a car's data, providing car_id

        :param int car_id: car ID
        :return: a dictionary representing a car
        :rtype: dict
        '''
        url = "/cars/{}".format(car_id)
        car = self.get(url)
        return car

    def updateCar(self, car_id: int, newCarVal):
        '''update a car, given its car_id and new value

        :param int car_id: car ID
        :param dict newCarVal: a dictionary containing keys and new values
        '''
        url = "/cars/{}/update".format(car_id)
        self.put(url, newCarVal)

    @staticmethod
    def transformLocation(lat, long_) -> tuple:
        '''transform coordinates with pos/neg sign to direction

        :param float lat: latitude, >0 means north, <0 means south
        :param float long_: longitude, >0 means east, <0 means west
        :return: transformed latitude and longitude strings
        :rtype: tuple
        '''
        if lat < 0:
            latS = "{} S".format(-lat)
        elif lat > 0:
            latS = "{} N".format(lat)
        if long_ < 0:
            longS = "{} W".format(-long_)
        elif long_ > 0:
            longS = "{} E".format(long_)
        return latS, longS