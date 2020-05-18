import unittest as _ut
import logging

logging.basicConfig(level=logging.DEBUG)

class TestUserManager(_ut.TestCase):
    def setUp(self):
        logger = logging.getLogger(f"{__name__}.setUp")
        from app.UserManager import UserManager
        self.uMgr = UserManager()
        self.conn = self.uMgr.conn
        # clear table
        with self.conn.cursor() as cur:
            cur.execute(f"delete from {UserManager.TABLE_NAME}")
        self.conn.commit()
        # insert test user data
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
        self.uMgr.addOne(dict(zip(
            ["username", "password", "fName", "lName", "email"],
            ["toBeDeleted", "wtfwtf", "Dummy", "Value", "user4@gmail.com"]
        )))
        self.usernames = ["stallylol", "shiyugun", "aspenrocks", "toBeDeleted"]

    def tearDown(self):
        logger = logging.getLogger(f"{__name__}.tearDown")
        # delete all inserted test data
        with self.conn.cursor() as cur:
            for username in self.usernames:
                cur.execute(f"delete from {self.uMgr.TABLE_NAME} where username = %s", username)
        self.conn.commit()

    def _countUsers(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT count(*) from {}".format(self.uMgr.TABLE_NAME))
            return cursor.fetchone()[0]

    def _userExists(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {self.uMgr.TABLE_NAME} WHERE username = %s", (username,))
            return cursor.fetchone()[0] == 1
    
    def testGetAll(self):
        '''confirm that number of records returned is same as number of 
        records in test_database
        '''
        self.assertEqual(self._countUsers(), len(self.uMgr.getMany({})))

    def testGetOne(self):
        # confirm true when user exists
        self.assertEqual('aspenrocks', self.uMgr.getOne('aspenrocks')["username"])
        # confirm that getItem() returns none when username not in db
        self.assertIsNone(self.uMgr.getOne("u34nonExistent"))

    def testAddOne(self):
        count = self._countUsers()
        success = self.uMgr.addOne(dict(zip(
            ["username", "password", 'fName', 'lName', "email"],
            ["papakase", "xxxyyy", "kaspian", "fitz", "user4@gmail.com"]
        )))
        self.assertTrue(success)
        self.assertTrue(count + 1, self._countUsers())

    def testAddOneDuplicateUsername(self):
        '''confirm repeat username is rejected due to primary key constraint'''
        from app.errors.api_exceptions import DuplicateKey
        with self.assertRaises(DuplicateKey):
            self.uMgr.addOne(dict(zip(
                ["username", "password", 'fName', 'lName', "email"],
                ["stallylol", "612345", "Stally", "Duan", "user.duplicate@gmail.com"]
            )))

    def testAddOneNullEmail(self):
        '''confirm null values are rejected due to not null constraint'''
        from app.errors.api_exceptions import InvalidArgument
        with self.assertRaises(InvalidArgument):
            self.uMgr.addOne(dict(zip(
                ["username", "password", 'fName', 'lName', "email"],
                ["papakase", "element", "kaspian", "fitz", None]
            )))

    def testUpdateOne(self):
        log = logging.getLogger(f"{__name__}.testUpdateOne")
        # update password
        log.debug(f"before updating, password is: {self.uMgr.getOne('stallylol')['password']}")
        self.assertTrue(self.uMgr.updateOne("stallylol", {"password": "111213"}))
        self.assertEqual("111213", self.uMgr.getOne("stallylol")["password"])

    def testUpdateOneNonExistentUser(self):
        # fail update becuase username does not exist
        self.assertFalse(self.uMgr.updateOne("someoneelse", {"password": "wrong"}))