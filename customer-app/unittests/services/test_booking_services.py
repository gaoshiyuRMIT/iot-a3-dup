import logging
import unittest as _ut
from unittest.mock import MagicMock, patch
from unittests import RESTFUL_API_URL
from . import mock_app

logger = logging.getLogger(__name__)

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


    def test_get_bookings_for_user(self):
        from app.services.BookingService import BookingService
        with patch.object(BookingService, "bookingsSortKey", lambda v: 1):
            with patch.object(BookingService, "post", return_value=self.bookings[:3]) as mock_post:
                bookings = BookingService().getBookingsForUser("janedoe1")
                self.assertEqual(self.bookings[:3], bookings)

    def test_add_booking(self):
        from app.services.BookingService import BookingService
        with patch.object(BookingService, "post", return_value={"booking_id": 31}) as mock_post:
            bk_id = BookingService().addBooking(self.bookings[0])
            self.assertEqual(31, bk_id)

    def test_update_booking(self):
        '''confirm that failure is propagated from `put` and update-booking returns false
        '''
        from app.services.BookingService import BookingService
        with patch.object(BookingService, "put", return_value={"success": False}) as mock_post:
            success = BookingService().updateBooking(17, self.bookings[1])
            self.assertFalse(success)

    def test_bookings_sort_key(self):
        '''confirm that the sorting key sorts bookings first by status (active ones first) and then by booking_id
        '''
        from app.services.BookingService import BookingService
        bookings = [{**d} for d in self.bookings]
        for i in range(len(bookings)):
            bookings[i]["booking_id"] = i + 1
        bookings.sort(key=BookingService.bookingsSortKey)
        statuses = [d['status'] for d in bookings]
        booking_ids = [d['booking_id'] for d in bookings]
        self.assertEqual(["booked", "booked"], statuses[:2])
        self.assertEqual([1, 5], booking_ids[:2])
        self.assertEqual(set(["finished", "finished", "cancelled"]), set(statuses[2:]))
