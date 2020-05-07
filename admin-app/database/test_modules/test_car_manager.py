#!/usr/bin/python3
import unittest
import logging
import sys
import pymysql as p
from iot.db_manager import DBManager
from iot.car_manager import CarManager

class TestCarManager(unittest.TestCase):
    USER = "root"
    PASSWORD = "toor"
    HOST =  "35.201.0.12"
    DATABASE = "TestPiDatabase"

    def setUp(self):
        self.connection = p.connect(TestCarManager.HOST, TestCarManager.USER, 
                                TestCarManager.PASSWORD, TestCarManager.DATABASE)
        with self.connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS Car")
            done = cursor.execute("""create table if not exists Car (
                        car_id INT not null auto_increment, 
                        year INT not null, 
                        car_model VARCHAR(32) not null,
                        body_type VARCHAR(32) not null,
                        num_seats INT not null, 
                        car_colour VARCHAR(32) not null,
                        cost_hour  DECIMAL(6,2) not null, 
                        latitude DECIMAL(38, 10), 
                        longitude DECIMAL(38, 10),
                        car_status VARCHAR(32) not null,  
                        PRIMARY KEY (car_id)
                        )""")
                       
            cursor.execute("""insert into Car (year, car_model, body_type, num_seats, 
                            car_colour, cost_hour) values (%s, %s, %s, %s, %s, %s)""",
                            (2020, "Honda", "sedan", 5, "yellow", 23.45,))
            cursor.execute("""insert into Car (year, car_model, body_type, num_seats, 
                            car_colour, cost_hour, latitude, longitude) values (%s, %s, %s, %s, %s, %s,
                            %s, %s)""",(2019, "Hyundai", "sedan", 5, "blue", 36.99, -37.813629, 144.963058,))
            cursor.execute("""insert into Car (year, car_model, body_type, num_seats, 
                            car_colour, cost_hour, latitude, longitude) values (%s, %s, %s, %s, %s, %s,
                            %s, %s)""",(2016, "Jeep", "truck", 8, "Red", 54.99, -38.150002, 144.350006,))
    
        self.connection.commit()


    def tearDown(self):
        try:
            self.connection.close()
        except Exception as e:
            print(str(e))
        finally:
            self.connection = None

    def countCars(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT count(*) from Car")
            return cursor.fetchone()[0]

    def carExists(self, car_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Car WHERE car_id = %s", (car_id,))
            return (cursor.fetchone()[0] == 1)

    def test_insertItem(self):
        with CarManager(self.connection) as db:
            count = self.countCars()
            # confirm can insert without lat&long
            self.assertTrue(db.insertItem(2000, "Kia", "sedan", 5, "orange", 30))
            count += 1
            self.assertTrue(count == self.countCars())
            # confirm can insert with lat&long
            self.assertTrue(db.insertItem(2010, "Ford", "wagon", 7, "brown", 31.12, -33.283577, 149.101273))
            count += 1
            self.assertTrue(count == self.countCars())

    def test_updateItem(self):
        log = logging.getLogger('UPDATEITEM')
        
        with CarManager(self.connection) as db:
            #update where lat and long are null
            self.assertTrue(db.updateItem(1, 66.160507, -153.369141))
            #update where lat and long already exist
            self.assertTrue(db.updateItem(2, -37.666666, 144.9999999))

    def test_getAll(self):
        log = logging.getLogger('GETALL')
        with CarManager(self.connection) as db:
            # confirm that number of records returned is same as number of 
            # records in test_database
            log.debug('VALUE SELF COUNT CARS = ' + str(self.countCars()))
            self.assertTrue(self.countCars() == len(db.getAll()))
            log.debug('OUTPUT DB.GETALL = ' + str(db.getAll()))

    def test_getAllBody(self):
        #log = logging.getLogger('GETALLBODY')
        with CarManager(self.connection) as db:
            #confirm the method returns correct number of cars with body_type...
            #log.debug('value sedan results: ' + str(db.getAllBody('sedan')))
            self.assertTrue(len(db.getAllBody('sedan')) == 2)
            self.assertTrue(len(db.getAllBody("truck")) == 1)

    def test_getItem(self):
        # confirm all entries added in setup exist in database
        log = logging.getLogger("GETITEM")
        car_id = 1
        #log.debug('value returned from car_id = 1 exists: ' + str(self.carExists(car_id)))
        self.assertTrue(self.carExists(car_id))
        #self.assertFalse(self.carExists(34))
        #self.assertTrue(self.carExists(2))
        #self.assertTrue(self.carExists(3))

        with CarManager(self.connection) as db:
            # confirm that the length of the tuple returned for car_id=1 is 1
            log.debug(str(db.getItem(car_id)))
            log.debug('tuple length item id = 1: ' + str(len(db.getItem(car_id))))
            #NOTE can't use len() function becuase returned tuple has extra brackets
            #not sure why the below returns an error but the class function works as expected
            self.assertEqual((len(db.getItem(car_id))) == 9)
            # confirm that getItem() does not return anything when car_id not in db
            self.assertIsNone(db.getItem(34))

    def test_deleteItem(self):
        #log = logging.getLogger('DELETE ITEM')
        count = self.countCars()
        #log.debug('initial car count '+ str(count))
        #confirm car_id = 1 is in db
        car_id = 1
        self.assertTrue(self.carExists(car_id))
        #log.debug('car_id 1 exists: ' + str((self.carExists(car_id))))
        with CarManager(self.connection) as db:
            # delete car
            self.assertTrue(db.deleteItem(car_id))
            #log.debug('deletecar: '+ str(db.deleteItem(car_id)))
            
            # confirm car no  longer in db
            #log.debug('does car 1 still exist post db.delete: '+str((self.carExists(car_id))))
            self.assertFalse(self.carExists(car_id))
            #confim record count has decreased by 1
            #log.debug('count number cars in db: ' + str(self.countCars()))
            self.assertTrue(self.countCars() == count-1)

def suite():
    #create a test suite which has all test methods in it
    #suite is an object
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCarManager)
    return suite

# tests = TestCarManager() 
# suite = tests.suite()
      
if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    runner = unittest.TextTestRunner(verbosity = 2)
    runner.run(suite())