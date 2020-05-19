#!/usr/bin/python3
import unittest
import logging
import sys
import pymysql as p
from iot.db_manager import DBManager
from iot.booking_manager import BookingManager

class TestBookingManager(unittest.TestCase):
    USER = "root"
    PASSWORD = "toor"
    HOST =  "35.201.0.12"
    DATABASE = "TestPiDatabase"

    def setUp(self):
        self.connection = p.connect(TestBookingManager.HOST, TestBookingManager.USER, 
                                    TestBookingManager.PASSWORD, TestBookingManager.DATABASE)
    
        with self.connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS Booking")
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS Booking ( 
                            booking_id INT not null AUTO_INCREMENT, 
                            username VARCHAR(32) not null,
                            car_id INT not null, 
                            date_booking DATE not null,
                            time_booking TIME not null,
                            date_return DATE not null,
                            time_return TIME not null,
                            status VARCHAR(32) not null,
                            
                            PRIMARY KEY (booking_id),
                            INDEX (username),
                            INDEX (car_id),
                            
                            FOREIGN KEY (username)
                                REFERENCES User(username),
                            
                            FOREIGN KEY (car_id)
                                REFERENCES Car(car_id)
                                ON UPDATE CASCADE ON DELETE CASCADE
                            )""")
            #because tear down of other database test classes does not remove the
            # test tables, they should still exist when creating this one, hence
            # foreign key constraints should be able to be satisfied
            cursor.execute("""insert into Booking (username, car_id, date_booking, 
                            time_booking, date_return, time_return, status) 
                            values (%s, %s, %s, %s, %s, %s, %s)""",
                             ("stallylol", 1, '2020-05-01', '09:14:23', 
                            '2020-05-02', '09:15:00', "booked"))
            cursor.execute("""insert into Booking (username, car_id, date_booking, 
                            time_booking, date_return, time_return, status)
                            values (%s, %s, %s, %s, %s, %s, %s)""",
                            ("stallylol", 2, '2020-04-01', '09:14:23', 
                            '2020-04-02', '09:15:00', "finished"))
            cursor.execute("""insert into Booking (username, car_id, date_booking, 
                            time_booking, date_return, time_return, status) 
                            values (%s, %s, %s, %s, %s, %s, %s)""",
                            ("shiyugun", 3, '2020-04-23', '09:14:23', 
                            '2020-04-25', '09:15:00', "cancelled"))
            cursor.execute("""insert into Booking (username, car_id, date_booking, 
                            time_booking, date_return, time_return, status) 
                            values (%s, %s, %s, %s, %s, %s, %s)""",
                            ("shiyugun", 1, '2020-03-01', '05:20:00', 
                            '2020-03-02', '06:15:00', "finished"))
            cursor.execute("""insert into Booking (username, car_id, date_booking, 
                            time_booking, date_return, time_return, status) 
                            values (%s, %s, %s, %s, %s, %s, %s)""",
                            ('aspenrocks', 2, '2020-05-04', '11:14:23', 
                            '2020-05-010', '12:15:00', "booked"))       
        self.connection.commit()


    def tearDown(self):
        try:
            self.connection.close()
        except Exception as e:
            print(str(e))
        finally:
            self.connection = None
            
    def countBookings(self):
        
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Booking")
            return cursor.fetchone()[0]
    
    def bookingExists(self, booking_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Booking WHERE booking_id = %s", (booking_id,))
            return cursor.fetchone()[0] == 1
    
    def test_getAll(self):
        log = logging.getLogger('GETALL')
        # count total number of records
        count = self.countBookings()
        log.debug('number of booking records: ' + str(count))
        with BookingManager(self.connection) as db:
            #confirm number of results from no arg call matches number of bookings
            self.assertTrue(len(db.getAll()) == count)
            
            # confirm that number of results returned matches number of specific
            # users/status category
            #database has been initailised with 2 entries for username 'stallylol'
            self.assertTrue(len(db.getAll('stallylol')) == 2)
            # database has one user 'aspenrocks' in it
            self.assertTrue(len(db.getAll('aspenrocks')) == 1)

            # confirm is returning correct number when user not there
            self.assertFalse(db.getAll('fakeuser'))

            #confirm returns correct result when supplied with user and status
            self.assertTrue(len(db.getAll('shiyugun', 'cancelled')) == 1)
            #confirm returns correct result when supplied with user and incorrect status keyword
            self.assertFalse(len(db.getAll('shiyugun', 'somethingwrong')) == 1)

    def test_getItem(self):
        log = logging.getLogger("GET ITEM")
        self.assertTrue(self.bookingExists(1))
        
        with BookingManager(self.connection) as db:
            # confirm method returns 1 when booking exists
            #log.debug('get item booking id = 1 output: ' + str(db.getItem(1)))
            #log.debug('LENGTH booking id = 1 output: ' + str(len(db.getItem(1))))
            self.assertTrue((len(db.getItem(1)))==8)
            # confirm that getItem() returns 0 when boooking_id not in db
            self.assertIsNone(db.getItem(34))
    
    def test_insertItem(self):
        
        count = self.countBookings()
        with BookingManager(self.connection) as db:
            # insert an item and cofirm row count has increased by 1
            self.assertTrue(db.insertItem("aspenrocks", 3, '2020-05-20', 
                            '10:00:00', '2020-05-25', '10:00:00'))
            self.assertTrue(self.countBookings() == count + 1)
    
    def test_updateItem(self):
        
        with BookingManager(self.connection) as db:
            #default updateItem changes status to finished - returns true 
            # if successful
            self.assertTrue(db.updateItem(1))
            # updateItem changing status to cancelled
            self.assertTrue(db.updateItem(5, 'cancelled'))


def suite():
    #create a test suite which has all test methods in it
    #suite is an object
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBookingManager)
    return suite
      
if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    runner = unittest.TextTestRunner(verbosity = 2)
    runner.run(suite())

        
