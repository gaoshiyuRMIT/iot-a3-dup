from .base_service import BaseService

class CarService(BaseService):
    def find_cars_with_issues(self):
        query = {"car_status": "hasIssue"}
        return self.search_cars(query)
    
    def search_cars(self, query: dict):
        url = "/cars/search"
        data = query
        cars = self.post(url, data)
        return cars

    def delete_car(self, car_id: int) -> bool:
        url = f"/cars/{car_id}"
        success = self.delete(url)
        return success

    def update_car(self, car_id: int, new_val: dict) -> bool:
        url = f"/cars/{car_id}"
        success = self.put(url, new_val)
        return success

    def add_car(self, new_val: dict) -> int:
        '''
        :return: car_id
        '''
        url = f"/cars/add"
        data = self.post(url, new_val)
        return data["car_id"]