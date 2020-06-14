import unittest as _ut
from unittest.mock import MagicMock, patch
from . import mock_app

class TestCarServices(_ut.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_app = mock_app

    def tearDown(self):
        self.__class__.mock_app.reset_mock()
    
    def setUp(self):
        self.cars = [
            dict(zip(
                ["year", "car_model", "body_type", "num_seats", "car_colour", "cost_hour", "car_status"],
                [2020, "Honda", "sedan", 5, "yellow", 23.45, "available"]
            )),
            dict(zip(
                ["year", "car_model", "body_type", "num_seats", "car_colour", "cost_hour", "latitude", "longitude", "car_status"],
                [2019, "Hyundai", "sedan", 5, "blue", 36.99, -37.813629, 144.963058, "available"]
            )),
            dict(zip(
                ["year", "car_model", "body_type", "num_seats", "car_colour", "cost_hour", "latitude", "longitude", "car_status"],
                [2016, "Jeep", "truck", 8, "Red", 54.99, -38.150002, 144.350006, "inUse"]
            ))
        ]

    def test_find_cars_with_issues(self):
        '''confirm that correct car_status is passed in the query and correct value is returned
        '''
        from app.services.car_service import CarService
        car = {**self.cars[0]}
        car["car_status"] = "hasIssue"
        with patch.object(CarService, "post", return_value=[car]) as mock_post:
            result = CarService().find_cars_with_issues()
            mock_post.assert_called_with("/cars/search", {"car_status": "hasIssue"})
            self.assertEqual([car], result)

    def test_report_car_with_issue(self):
        '''confirm that car_status change is passed to the correct endpoint & success is propagated when status is 200
        '''
        from app.services.car_service import CarService
        with patch.object(CarService, "put", return_value=True) as mock_put:
            success = CarService().report_car_with_issue(1)
            self.assertTrue(success)
            mock_put.assert_called_with("/cars/1/update", {"car_status": "hasIssue"})

    def test_search_cars(self):
        '''confirm that correct cars are returned when status is 200
        '''
        from app.services.car_service import CarService
        with patch.object(CarService, "post", return_value=self.cars[:2]):
            result = CarService().search_cars({"cost_hour": ["", 40]})
            self.assertEqual(self.cars[:2], result)

    def test_delete_car(self):
        '''confirm that correct car is deleted and success is propagated is status code is 200
        '''
        from app.services.car_service import CarService
        with patch.object(CarService, "delete", return_value=True) as mock_del:
            result = CarService().delete_car(2)
            self.assertTrue(result)
            mock_del.assert_called_with("/cars/2")

    def test_update_car(self):
        '''confirm that correct updated value is passed and success is propagated if status code is 200
        '''
        from app.services.car_service import CarService
        with patch.object(CarService, "put", return_value=True) as mock_put:
            result = CarService().update_car(3, {"cost_hour": 39.5})
            self.assertTrue(result)
            mock_put.assert_called_with("/cars/3/update", {"cost_hour": 39.5})

    def test_add_car(self):
        '''confirm that new car value is passed the the add car endpoint and car_id is returned if status is 200
        '''
        from app.services.car_service import CarService
        car = {**self.cars[2]}
        car["car_colour"] = "silver"
        with patch.object(CarService, "post", return_value={"car_id": 4}) as mock_post:
            result = CarService().add_car(car)
            self.assertEqual(4, result)
            mock_post.assert_called_with("/cars/add", car)

    def test_get_car(self):
        '''confirm that the correct car is returned if status is 200
        '''
        from app.services.car_service import CarService
        with patch.object(CarService, "get", return_value=self.cars[1]) as mock_get:
            result = CarService().get_car(2)
            self.assertEqual(self.cars[1], result)
            mock_get.assert_called_with("/cars/2", {})