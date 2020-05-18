import logging
import unittest as _ut
from unittest.mock import patch

from . import mock_jsonify
from app.errors.api_exceptions import MissingKey


logger = logging.getLogger(__name__)

class TestBookingsRoute(_ut.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_jsonify = mock_jsonify

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

    def tearDown(self):
        self.__class__.mock_jsonify.reset_mock()

    def testSearchBookings(self):
        '''confirm that the correct query dictionary is passed to booking manager's getMany method, 
        and correct result is returned by view function
        '''
        query = {"username": "stallylol", "car_id": 1, "status": "booked", 
                "date_booking": ["2020-05-01", "2020-06-01"]}
        from app.BookingManager import BookingManager
        with patch.object(BookingManager, 'keepValidFieldsOnly', return_value=query):
            with patch.object(BookingManager, 'getMany', return_value=self.bookings[0]) as mock_get_many:
                from app.routes.bookings import bookings
                bookings()
                mock_get_many.assert_called_with(query)
                self.mock_jsonify.assert_called_with({"data": self.bookings[0]})

    def testSearchBookingsNoneValue(self):
        '''confirm that None and empty values in query dictionary are ignored
        '''
        query = {"date_return": [], "username": "", "status": None, "car_id": 17}
        from app.BookingManager import BookingManager
        with patch.object(BookingManager, 'keepValidFieldsOnly', return_value=query):
            with patch.object(BookingManager, 'getMany') as mock_get_many:
                from app.routes.bookings import bookings
                bookings()
                mock_get_many.assert_called_with({"car_id": 17})

    def testUpdateBooking(self):
        '''confirm that the correct booking data is passed to booking manager's updateOne method
        '''
        booking = self.bookings[0]
        from app.BookingManager import BookingManager
        with patch.object(BookingManager, 'keepValidFieldsOnly', return_value=booking):
            with patch.object(BookingManager, 'updateOne') as mock_update_one:
                from app.routes.bookings import updateBooking
                updateBooking(23)
                mock_update_one.assert_called_with(23, booking)

    def testUpdateBookingNoneValue(self):
        '''confirm that None and empty values in the new booking data are ignored
        '''
        booking = {"date_return": None, "status": "", "time_return": "19:00:00"}
        from app.BookingManager import BookingManager
        with patch.object(BookingManager, 'keepValidFieldsOnly', return_value=booking):
            with patch.object(BookingManager, 'updateOne') as mock_update_one:
                from app.routes.bookings import updateBooking
                updateBooking(23)
                mock_update_one.assert_called_with(23, {"time_return": "19:00:00"})

    def testUpdateNonExistentBooking(self):
        '''confirm that when providing a non-existent booking_id, the view function returns failure
        '''
        from app.BookingManager import BookingManager
        with patch.object(BookingManager, 'updateOne', return_value=False):
            from app.routes.bookings import updateBooking
            updateBooking(23)
            self.mock_jsonify.assert_called_with({"data": {"success": False}})

    def testGetBooking(self):
        '''confirm that the correct booking data is passed to booking manager's getOne method
        '''
        from app.BookingManager import BookingManager
        with patch.object(BookingManager, 'getOne') as mock_get_one:
            from app.routes.bookings import getBooking
            getBooking(31)
            mock_get_one.assert_called_with(31)

    def testGetNonExistentBooking(self):
        '''confirm that when providing a non-existent booking_id, the view function raises an exception
        '''
        from app.BookingManager import BookingManager
        with patch.object(BookingManager, 'getOne', return_value=None):
            from app.routes.bookings import getBooking
            with self.assertRaises(MissingKey):
                getBooking(31)

    def testAddBooking(self):
        '''confirm that booking manager's addOne is passed the correct data
        '''
        from app.BookingManager import BookingManager
        with patch.object(BookingManager, 'keepValidFieldsOnly', return_value=self.bookings[1]):
            with patch.object(BookingManager, 'addOne') as mock_add_one:
                from app.routes.bookings import addBooking
                addBooking()
                mock_add_one.assert_called_with(self.bookings[1])

    def testAddBookingReturnId(self):
        '''confirm that when adding is successful, booking_id is returned by the view function
        '''
        from app.BookingManager import BookingManager
        with patch.object(BookingManager, 'addOne', return_value=43):
            from app.routes.bookings import addBooking
            addBooking()
            self.mock_jsonify.assert_called_with({"data": {"booking_id": 43}})

    def testAddBookingIgnoreId(self):
        '''confirm that if booking_id is provided in the booking data, it is ignored
        '''
        booking = {**self.bookings[3]}
        booking["booking_id"] = 37
        from app.BookingManager import BookingManager
        with patch.object(BookingManager, 'keepValidFieldsOnly', return_value=booking):
            with patch.object(BookingManager, 'addOne') as mock_add_one:
                from app.routes.bookings import addBooking
                addBooking()
                mock_add_one.assert_called_with(self.bookings[3])
                self.assertNotIn("booking_id", self.bookings[3])