import unittest as _ut
import logging
from datetime import date, timedelta

logging.basicConfig(level=logging.DEBUG)

class TestBookingManager(_ut.TestCase):
    def setUp(self):
        from app.BookingManager import BookingManager
        from app.UserManager import UserManager
        from app.CarManager import CarManager
        self.bkMgr = BookingManager()
        self.uMgr = UserManager()
        self.cMgr = CarManager()
        self.conn = self.bkMgr.conn
        self.bk_ids = [-1,-1,-1,-1,-1]
        self.car_ids = [-1] * 3
        self.usernames = []
        # firstly clear table
        with self.conn.cursor() as cur:
            cur.execute("delete from {}".format(BookingManager.TABLE_NAME))
            cur.execute("delete from {}".format(CarManager.TABLE_NAME))
            cur.execute("delete from {}".format(UserManager.TABLE_NAME))
        self.conn.commit()
        # insert test user data
        self._insertUsers()
        # insert test car data
        self._insertCars()
        # insert test booking data
        values = [
            ["stallylol", self.car_ids[0], '2020-05-01', '09:14:23', '2020-05-02', '09:15:00', "booked"],
            ["stallylol", self.car_ids[1], '2020-04-01', '09:14:23', '2020-04-02', '09:15:00', "finished"],
            ["shiyugun", self.car_ids[2], '2020-04-23', '09:14:23', '2020-04-25', '09:15:00', "cancelled"],
            ["shiyugun", self.car_ids[0], '2020-03-01', '05:20:00', '2020-03-02', '06:15:00', "finished"],
            ['aspenrocks', self.car_ids[1], '2020-05-04', '11:14:23', '2020-05-010', '12:15:00', "booked"]
        ]
        for i in range(5):
            self.bk_ids[i] = self.bkMgr.addOne(dict(zip(
                ["username", "car_id", "date_booking", "time_booking", "date_return", 
                "time_return", "status"],
                values[i]
            )))

    def _insertCars(self):
        self.car_ids[0] = self.cMgr.addOne(dict(zip(
            ["year", "car_model", "body_type", "num_seats", "car_colour", "cost_hour", "car_status"],
            [2020, "Honda", "sedan", 5, "yellow", 23.45, "available"]
        )))
        self.car_ids[1] = self.cMgr.addOne(dict(zip(
            ["year", "car_model", "body_type", "num_seats", "car_colour", "cost_hour", "latitude", "longitude", "car_status"],
            [2019, "Hyundai", "sedan", 5, "blue", 36.99, -37.813629, 144.963058, "available"]
        )))
        self.car_ids[2] = self.cMgr.addOne(dict(zip(
            ["year", "car_model", "body_type", "num_seats", "car_colour", "cost_hour", "latitude", "longitude", "car_status"],
            [2016, "Jeep", "truck", 8, "Red", 54.99, -38.150002, 144.350006, "available"]
        )))


    def _insertUsers(self):
        self.usernames = ["stallylol", "shiyugun", "aspenrocks"]
        self.uMgr.addOne(dict(zip(
            ["username", "password", "fName", "lName", "email"],
            ["stallylol", "123456", "Stally", "Duan", "user1@gmail.com"]
        )))
        self.uMgr.addOne(dict(zip(
            ["username", "password", "fName", "lName", "email"],
            ["shiyugun", "abcdef", "Shiyu", "Gao", "user2@gmail.com"]
        )))
        self.uMgr.addOne(dict(zip(
            ["username", "password", "fName", "lName", "email"],
            ["aspenrocks", "78910", "Aspen", "Forster", "user3@gmail.com"]
        )))

    def tearDown(self):
        # clear booking table
        with self.conn.cursor() as cur:
            for bk_id in self.bk_ids:
                cur.execute(f"delete from {self.bkMgr.TABLE_NAME} where booking_id = %s", bk_id)
            for car_id in self.car_ids:
                cur.execute(f"delete from {self.cMgr.TABLE_NAME} where car_id = %s", car_id)
            for username in self.usernames:
                cur.execute(f"delete from {self.uMgr.TABLE_NAME} where username = %s", username)
        self.conn.commit()

    def _countBookings(self):
        with self.conn.cursor() as cursor:
            cursor.execute("select count(*) from {}".format(self.bkMgr.TABLE_NAME))
            return cursor.fetchone()[0]

    def _bookingExists(self, booking_id):
        with self.conn.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {self.bkMgr.TABLE_NAME} WHERE booking_id = %s", (booking_id,))
            return cursor.fetchone()[0] == 1

    def testGetAll(self):
        log = logging.getLogger(f"{__name__}.testGetAll")
        # count total number of records
        count = self._countBookings()
        log.debug('number of booking records: ' + str(count))
        # confirm number of results from no arg call matches number of bookings
        self.assertEqual(count, len(self.bkMgr.getMany({})))

    def testGetAllForUser(self):
        # confirm that number of results returned matches number of specific users category
        self.assertEqual(2, len(self.bkMgr.getMany({"username": "stallylol"})))
        self.assertEqual(1, len(self.bkMgr.getMany({"username": "aspenrocks"})))
        # confirm it returns zero entries when getting bookings for a non-existent user
        self.assertEqual(0, len(self.bkMgr.getMany({"username": "fakeuser"})))

    def testGetAllForUserFilterByStatu(self):
        # confirm returns correct result when supplied with user and status
        bookings = self.bkMgr.getMany({"username": "shiyugun", "status": "cancelled"})
        self.assertEqual(1, len(bookings))
        # confirm returns correct result when supplied with user and incorrect status keyword
        self.assertEqual(0, len(self.bkMgr.getMany({"username": 'shiyugun', "status": 'somethingwrong'})))

    def testGetOne(self):
        '''check that `getOne` returns an item when supplying valid booking_id,
        and the returned item has the correct keys
        '''
        log = logging.getLogger(f"{__name__}.testGetOne")
        booking = self.bkMgr.getOne(self.bk_ids[0])
        self.assertTrue(self._bookingExists(self.bk_ids[0]))
        self.assertEqual(
            set(["booking_id", "username", "car_id", "date_booking", "time_booking", "date_return", 
                "time_return", "status"]),
            set(booking.keys())
        )
    
    def testGetOneNonExistent(self):
        '''confirm that `getOne` returns None when booking_id not in db'''
        nonExistentId = self.bk_ids[-1] + 10
        self.assertIsNone(self.bkMgr.getOne(nonExistentId))

    def testAddOne(self):
        count = self._countBookings()
        newBooking = dict(zip(
            ["username", "car_id", "date_booking", "time_booking", "date_return", 
                "time_return", "status"],
            ["aspenrocks", self.car_ids[2], '2020-05-20', '10:00:00', '2020-05-25', '10:00:00', "booked"]
        ))
        bk_id = self.bkMgr.addOne(newBooking)
        self.bk_ids.append(bk_id)
        booking = self.bkMgr.getOne(bk_id)
        self.assertEqual(dict(**newBooking, booking_id=bk_id), booking)
        self.assertEqual(count + 1, self._countBookings())

    def testUpdateOneChangeStatus(self):
        # change status to 'finished'
        self.assertTrue(self.bkMgr.updateOne(self.bk_ids[0], {"status": "finished"}))
        self.assertTrue(self.bkMgr.updateOne(self.bk_ids[4], {"status": "cancelled"}))

    def testTransformDateTime(self):
        '''confirm that BookingManager.tranformDateTime transforms date & time from db format to ISO string
        '''
        booking = {
            "date_booking": date(2020,1,1), 
            "time_booking": timedelta(hours=19)
        }
        result = self.bkMgr.tranformDateTime(booking)
        self.assertEqual(
            {"date_booking": "2020-01-01", "time_booking": "19:00:00"},
            result
        )