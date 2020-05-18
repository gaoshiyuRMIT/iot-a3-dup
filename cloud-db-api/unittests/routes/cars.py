import logging
import unittest as _ut
from unittest.mock import patch

from . import mock_jsonify

logger = logging.getLogger(__name__)


class TestCarsRoute(_ut.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_jsonify = mock_jsonify

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
                [2016, "Jeep", "truck", 8, "Red", 54.99, -38.150002, 144.350006, "available"]
            ))
        ]

    def tearDown(self):
        self.__class__.mock_jsonify.reset_mock()

    def testJsonifyDecorator(self):
        '''confirm that the jsonify decorator transform the return data of view functions to json strings
        '''
        from app.CarManager import CarManager
        with patch.object(CarManager, 'getMany', return_value=self.cars):
            from app.routes.cars import cars
            cars()
            self.mock_jsonify.assert_called_with(
                {"data": self.cars}
            )

    def testSearchCarsFilterNoneValue(self):
        '''confirm that None values and empty strings in the query dictionary is ignored
        '''
        query = {"car_model": "hyundai", "body_type": "", "car_colour": None, "cost_hour": []}
        from app.CarManager import CarManager
        with patch.object(CarManager, 'keepValidFieldsOnly', return_value=query):
            with patch.object(CarManager, 'getMany') as mock_get_many:
                from app.routes.cars import cars
                cars()
                mock_get_many.assert_called_with({"car_model": "hyundai"})

    def testUpdateCar(self):
        '''check that the correct car data is passed to car manager updateOne method
        '''
        newCar = {**self.cars[2]}
        car_id = 17
        from app.CarManager import CarManager
        with patch.object(CarManager, 'keepValidFieldsOnly', return_value=newCar):
            with patch.object(CarManager, 'updateOne') as mock_update_one:
                from app.routes.cars import updateCar
                updateCar(car_id)
                mock_update_one.assert_called_with(car_id, newCar)

    def testUpdateCarNoneValue(self):
        '''confirm that None and empty values in filter dictionary are ignored
        '''
        newCar = {"car_colour": "", "body_type": None, "status": "inUse"}
        from app.CarManager import CarManager
        with patch.object(CarManager, 'keepValidFieldsOnly', return_value=newCar):
            with patch.object(CarManager, 'updateOne') as mock_update_one:
                from app.routes.cars import updateCar
                updateCar(17)
                mock_update_one.assert_called_with(17, {"status": "inUse"})

    def testUpdateNonExistentCar(self):
        '''confirm that the view function returns failure when the car_id does not exist
        '''
        from app.CarManager import CarManager
        with patch.object(CarManager, 'updateOne', return_value=False):
            from app.routes.cars import updateCar
            updateCar(13)
            self.mock_jsonify.assert_called_with({"data": {"success": False}})

    def testGetCar(self):
        '''confirm that the correct car_id is passed to car manager getOne method
        '''
        from app.CarManager import CarManager
        with patch.object(CarManager, 'getOne') as mock_get_one:
            from app.routes.cars import getCar
            getCar(19)
            mock_get_one.assert_called_with(19)

    def testGetNonExistentCar(self):
        '''confirm that a MissingKey exception is raised when providing a non-existent car_id
        '''
        from app.errors.api_exceptions import MissingKey
        from app.CarManager import CarManager
        with patch.object(CarManager, 'getOne', return_value=None):
            from app.routes.cars import getCar
            with self.assertRaises(MissingKey):
                getCar(23)

    def testAddCar(self):
        '''confirm that the correct new car data is passed to car manager addOne method
        '''
        from app.CarManager import CarManager
        car = self.cars[1]
        with patch.object(CarManager, 'keepValidFieldsOnly', return_value=car):
            with patch.object(CarManager, 'addOne') as mock_get_one:
                from app.routes.cars import addCar
                addCar()
                mock_get_one.assert_called_with(car)

    def testAddCarReturnCarId(self):
        '''confirm that the car_id of the newly added car is returned by the view function given adding is successful
        '''
        from app.CarManager import CarManager
        with patch.object(CarManager, 'addOne', return_value=19):
            from app.routes.cars import addCar
            addCar()
            self.mock_jsonify.assert_called_with({"data": {"car_id": 19}})
