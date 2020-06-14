import unittest as ut
import logging


logging.basicConfig(level=logging.DEBUG)

class TestEmployeeManager:
 FIELDS = ["username", "password", "fName", "lName", "email", "role"]
    PK = "username"
    TABLE_NAME = "Employee"

    def setup(self):
        '''
        set up connection, clear test table and insert data for testing. 
        '''
        from app.employee_manager import EmployeeManager
        self.empMgr = EmployeeManager()
        self.conn = self.empMgr.conn
        #clear test table
        with self.conn.cursor() as cursor:
            cursor.execute("delete from {}".format(self.empMgr.TABLE_NAME))
        self.conn.commit()
        #add test data
        self.dataIDs = [-1, -1, -1]
        self.dataID[0] = self.empMgr.addOne(dict(zip(["username", "password", "fName", "lName", "email", "role"], 
        ['aspen1','Test','Aspen','Forster','aspenforster@gmail.com', 'admin'] )))
         self.dataID[1] = self.empMgr.addOne(dict(zip(["username", "password", "fName", "lName", "email", "role"], 
        ('shiyu','root','Shiyu','Gao','shiyu@test.com', 'manager'] )))
         self.dataID[2] = self.empMgr.addOne(dict(zip(["username", "password", "fName", "lName", "email", "role"], 
        ['stally_admin','toor','Stally','Neil','stally@test.com', 'engineer'] )))
        
    def tearDown(self):
        # clear employee table
        with self.conn.cursor() as cur:
            for dataID in self.dataIDs:
                cur.execute(f"delete from {self.empMgr.TABLE_NAME} where activity_id = %s", dataID)
        self.conn.commit()

    def _empExists(self, car_id):
        '''check whether a record with specified employee is present in the car table
        '''
        from app.employee_manager import EmployeeManager
        empMgr = EmployeeManager()
        with self.conn.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {empMgr.TABLE_NAME} WHERE username = %s", (username,))
            return (cursor.fetchone()[0] == 1)
        
    def testGetOne(self):
        '''by calling `EmployeerManager.getOne`,
        1. confirm all entries added in setup exist in database
        2. confirm the returned item has the correct keys
        '''
        log = logging.getLogger(f"{__name__}.testGetOne")
        username = aspen1
        emp = self.empMgr.getOne(aspen1)
        self.assertTrue(self._carExists(username))
        
