import unittest as _ut
import logging
from . import patch_flask_g

logging.basicConfig(level=logging.DEBUG)


class TestCarManager(_ut.TestCase):
    @patch_flask_g()
    def setUp(self):
        '''set instance variable car manager, connection and car id list,
        clear car table, and insert test car data
        '''
        from app.CarManager import CarManager
        self.cMgr = CarManager()
        self.conn = self.cMgr.conn
        self.car_ids = [-1, -1, -1]
        # firstly clear table
        with self.conn.cursor() as cur:
            cur.execute("delete from {}".format(CarManager.TABLE_NAME))
        self.conn.commit()
        # insert test car data & record car_ids
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


    def tearDown(self):
        '''delete inserted test data from car table
        '''
        logger = logging.getLogger(f"{__name__}.tearDown")
        with self.conn.cursor() as cur:
            for cid in self.car_ids:
                cur.execute(f"delete from {self.cMgr.TABLE_NAME} where car_id = %s", cid)
        self.conn.commit()

    def _countCars(self):
        '''get total number of records in the car table
        '''
        from app.CarManager import CarManager
        with self.conn.cursor() as cursor:
            cursor.execute(f"SELECT count(*) from {CarManager.TABLE_NAME}")
            return cursor.fetchone()[0]

    def _carExists(self, car_id):
        '''check whether a record with specified car_id is present in the car table
        '''
        from app.CarManager import CarManager
        with self.conn.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {CarManager.TABLE_NAME} WHERE car_id = %s", (car_id,))
            return (cursor.fetchone()[0] == 1)

    def testUpdateLocation(self):   
        '''update the coordinates of a car, which either already has location or does not
        '''    
        #update where lat and long are null
        self.assertTrue(self.cMgr.updateOne(self.car_ids[0], {"latitude": 66.160507, "longitude": -153.369141}))
        #update where lat and long already exist
        self.assertTrue(self.cMgr.updateOne(self.car_ids[1], {"latitude": -37.666666, "longitude": 144.9999999}))

    def testGetAll(self):
        '''get many cars without any filter
        '''
        log = logging.getLogger(f"{__name__}.testGetAll")
        # confirm that number of records returned is same as number of 
        # records in test_database
        exp = self._countCars()
        act = len(self.cMgr.getMany({}))
        log.debug("VALUE SELF COUNT CARS = {}".format(exp))
        self.assertEqual(exp, act)
        log.debug('OUTPUT CMGR.GETALL = {}'.format(act))

    def testGetAllBody(self):
        '''get many cars, filtering by body_type,
        confirm the method returns correct number of cars with body_type...
        '''
        self.assertEqual(2, len(self.cMgr.getMany({"body_type": "sedan"})))
        self.assertEqual(1, len(self.cMgr.getMany({"body_type": "truck"})))
        
    def testGetOne(self):
        '''by calling `CarManager.getOne`,
        1. confirm all entries added in setup exist in database
        2. confirm the returned item has the correct keys
        '''
        log = logging.getLogger(f"{__name__}.testGetOne")
        car_id = self.car_ids[0]
        car = self.cMgr.getOne(car_id)
        self.assertTrue(self._carExists(car_id))
        self.assertEqual(
            set(["car_id", "year", "car_model", "body_type", "num_seats", "car_colour", "cost_hour", 
            "latitude", "longitude", "car_status"]), 
            set(car.keys())
        )
