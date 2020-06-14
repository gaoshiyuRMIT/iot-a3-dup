from datetime import date, timedelta
import unittest as _ut
from unittest.mock import MagicMock, patch
from . import mock_app

class TestBookingServices(_ut.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_app = mock_app

    def tearDown(self):
        self.__class__.mock_app.reset_mock()
    
    def setUp(self):
        values = [
            ["stallylol", 1, '2020-05-01', '09:14:23', '2020-05-02', '09:15:00', "booked"],
            ["stallylol", 2, '2020-04-01', '09:14:23', '2020-04-02', '09:15:00', "finished"],
            ["shiyugun", 3, '2020-04-23', '09:14:23', '2020-04-25', '09:15:00', "cancelled"],
            ["shiyugun", 1, '2020-03-01', '05:20:00', '2020-03-02', '06:15:00', "finished"],
            ['aspenrocks', 2, '2020-05-04', '11:14:23', '2020-05-010', '12:15:00', "booked"]
        ]
        keys = ["username", "car_id", "date_booking", "time_booking", "date_return",  "time_return", "status"]
        self.bookings = [dict(zip(keys, v)) for v in values]
        self.cars = [
            dict(zip(
                ["car_id", "year", "car_model", "body_type", "num_seats", "car_colour", "cost_hour", "car_status"],
                [1, 2020, "Honda", "sedan", 5, "yellow", 23.45, "available"]
            ))
        ]

    def test_get_bookings_for_car(self):
        '''test that POST is used and correct values are returned
        '''
        from app.services.booking_service import BookingService
        expected = [self.bookings[0], self.bookings[3]]
        with patch.object(BookingService, "post", return_value=expected) as mock_post:
            result = BookingService().get_bookings_for_car(1)
            self.assertEqual(expected, result)
    
    def test_search_bookings(self):
        '''confirm that correct query is passed to `post` and return value is propagated
        '''
        from app.services.booking_service import BookingService
        with patch.object(BookingService, "post", return_value=self.bookings[:2]):
            result = BookingService().search_bookings({"username": "stallylol"})
            self.assertEqual(self.bookings[:2], result)

    def test_transform_date(self):
        '''confirm that date string is tranformed into date object
        '''
        from app.services.booking_service import BookingService
        booking = {**self.bookings[0]}
        booking['date_booking'] = "2020-02-02"
        booking["date_return"] = '2020-03-03'
        BookingService().transform_date(booking)
        self.assertEqual(date(2020, 2, 2), booking["date_booking"])
        self.assertEqual(date(2020, 3, 3), booking["date_return"])

    def test_transform_time(self):
        '''confirm that time string is converted into timedelta object
        '''
        from app.services.booking_service import BookingService
        booking = {**self.bookings[0]}
        booking["time_booking"] = "00:02:00"
        booking["time_return"] = "03:00:01"
        BookingService().transform_time(booking)
        self.assertEqual(timedelta(seconds=2 * 60), booking['time_booking'])
        self.assertEqual(timedelta(seconds=3 * 3600 + 1), booking["time_return"])

    def test_gen_date_str(self):
        '''confirm that the method generates the correct date string from date object
        '''
        from app.services.booking_service import BookingService
        result = BookingService().gen_date_str(date(2020,1,2))
        self.assertEqual("2020-01-02", result)

    def test_get_all_with_cars(self):
        '''confirm that car info is returned along with booking info
        '''
        from app.services.booking_service import BookingService
        bookings = [self.bookings[0], self.bookings[3]]
        for b in bookings:
            b.update(self.cars[0])
        with patch.object(BookingService, "get", return_value=bookings):
            result = BookingService().get_all_with_cars()
            self.assertEqual(bookings, result)