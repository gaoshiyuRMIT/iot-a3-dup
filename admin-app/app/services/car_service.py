from urllib.parse import quote
from .base_service import BaseService

class CarService(BaseService):
    def find_cars_with_issues(self):
        '''find all cars reported with issues

        :return: all cars with issues
        :rtype: list
        '''
        query = {"car_status": "hasIssue"}
        return self.search_cars(query)
    
    def report_car_with_issue(self, car_id):
        '''report a car with issue, given car ID

        :param int car_id: car ID
        :rtype: bool
        :return: whether the update is successful
        '''
        return self.update_car(car_id, {"car_status": "hasIssue"})

    def search_cars(self, query: dict):
        '''search for cars given query dictionary

        :param dict query: key-value map that specifies the value/range that a car's fields need to match
        :rtype: list
        :return: all cars that satisfy the query
        '''
        url = "/cars/search"
        data = query
        cars = self.post(url, data)
        return cars

    def delete_car(self, car_id: int) -> bool:
        '''given car_id, delete a car

        :param int car_id: car ID
        :return: whether the deletion is successful
        :rtype: bool
        '''
        url = f"/cars/{car_id}"
        success = self.delete(url)
        return success

    def update_car(self, car_id: int, new_val: dict) -> bool:
        '''given car_id and new car values, update a car

        :param int car_id: ID of car to update
        :param dict new_val: new key-value map to update the car to be
        :return: whether the update is successful
        :rtype: bool
        '''
        url = f"/cars/{car_id}/update"
        success = self.put(url, new_val)
        return success

    def add_car(self, new_val: dict) -> int:
        '''add a car, given new car values

        :param dict new_val: key-value map representing a car to be added
        :return: car_id of the newly added car
        :rtype: int
        '''
        url = f"/cars/add"
        data = self.post(url, new_val)
        return data["car_id"]

    def get_car(self, car_id) -> dict:
        '''get a car's info by car_id
        
        :param int car_id: car ID
        :return: key-value map representing a car
        :rtype: dict
        '''
        url = f"/cars/{car_id}"
        return self.get(url, {})