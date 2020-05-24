import logging
import unittest as _ut
from unittest.mock import MagicMock, patch
from unittests import RESTFUL_API_URL
from . import mock_app

logger = logging.getLogger(__name__)


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

    def test_get_all_available_cars(self):
        '''confirm that available and only available cars are returned
        '''
        from app.services.CarService import CarService
        with patch.object(CarService, "post", return_value=self.cars[:2]):
            cars = CarService().getAllAvailableCars()
            self.assertEqual(self.cars[:2], cars)

    def test_search_cars_by_id(self):
        '''confirm that searching cars by car_id passes the correct args to `post`
        '''
        from app.services.CarService import CarService
        with patch.object(CarService, "post", return_value=self.cars[:1]) as mock_post:
            cars = CarService().searchCars({"car_id": 1})
            mock_post.assert_called_with("/cars/search", {"car_id": 1})
            self.assertEqual(self.cars[:1], cars)

    def test_search_cars_by_cost_hour_range(self):
        '''confirm that when providing the range of cost per hour, the correct data is returned
        '''
        from app.services.CarService import CarService
        with patch.object(CarService, "post", return_value=[self.cars[1]]) as mock_post:
            cars = CarService().searchCars({"cost_hour": [30, 40]})
            mock_post.assert_called_with("/cars/search", {"cost_hour": [30, 40]})
            self.assertEqual([self.cars[1]], cars)

    def test_get_one_car(self):
        '''confirm that getting one car by id returns the correct car
        '''
        from app.services.CarService import CarService
        with patch.object(CarService, "get", return_value=self.cars[0]) as mock_get:
            car = CarService().getCar(71)
            mock_get.assert_called_with("/cars/71")
            self.assertEqual(self.cars[0], car)

    def test_update_one_car(self):
        '''confirm that when providing car_id and new values, the car is updated and success is returned
        '''
        from app.services.CarService import CarService
        with patch.object(CarService, "put", return_value=self.cars[0]) as mock_put:
            success = CarService().updateCar(13, self.cars[1])
            self.assertTrue(success)
            mock_put.assert_called_with("/cars/13/update", self.cars[1])

    def test_transform_location(self):
        '''confirm that numeric coordinates are transformed into user-friendly strings
        '''
        from app.services.CarService import CarService
        self.assertEqual(
            ("100.1 S", "50.2 E"),
            CarService.transformLocation(-100.1, 50.2)
        )