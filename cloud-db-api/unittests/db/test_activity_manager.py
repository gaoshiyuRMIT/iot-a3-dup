import unittest as ut
import logging


logging.basicConfig(level=logging.DEBUG)

class TestActivityManager:

    def setUp(self):
        '''
        set up connection, clear test table and insert data for testing. 
        '''
        from app.ActivityManager import ActivityManager
        self.actMgr = ActivityManager()
        self.conn = self.actMgr.conn
        #clear test table
        with self.conn.cursor() as cursor:
            cursor.execute("delete from {}".format(self.actMgr.TABLE_NAME))
        self.conn.commit()
        #add test data
        self.dataIDs = [-1, -1, -1, -1, -1]
        self.dataID[0] = self.actMgr.addOne(dict(zip(["username", "activity"], 
        ["Stally", 'login'] )))
        self.dataID[1] = self.actMgr.addOne(dict(zip(["username", "activity"], 
        ["Stally", 'login'] )))
        self.dataID[2] = self.actMgr.addOne(dict(zip(["username", "activity"], 
        ["Aspen", 'register'] )))
        self.dataID[3] = self.actMgr.addOne(dict(zip(["username", "activity"], 
        ["Shiyu", 'add_booking'] )))
        self.dataID[4] = self.actMgr.addOne(dict(zip(["username", "activity"], 
        ["stallylol", 'add_booking'] )))

    def tearDown(self):
        # clear booking table
        with self.conn.cursor() as cur:
            for dataID in self.dataIDs:
                cur.execute(f"delete from {self.actMgr.TABLE_NAME} where activity_id = %s", dataID)
        self.conn.commit()
    
    def testCountActivityType(self):
        '''test whether activity manager counts number of activity events correctly'''
        self.assertEqual(3, len(self.actMgr.get_type_counts()))


    
