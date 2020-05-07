#!/usr/bin/python3
import unittest
import pymysql as p
import logging
import sys
from iot.db_manager import DBManager
from iot.user_manager import UserManager

class TestUserManager(unittest.TestCase):
    USER = "root"
    PASSWORD = "toor"
    HOST =  "35.201.0.12"
    DATABASE = "TestPiDatabase"

    def setUp(self):
        self.connection = p.connect(TestUserManager.HOST, TestUserManager.USER, 
                                TestUserManager.PASSWORD, TestUserManager.DATABASE)
    
        with self.connection.cursor() as cursor:
            cursor.execute("drop table if exists User")
            cursor.execute(""" create table if not exists User (
                        username VARCHAR(32) not null, 
                        password VARCHAR(255) not null, 
                        fName VARCHAR(32) not null,
                        lName VARCHAR(32) not null,
                        email VARCHAR(255) not null,   
                        PRIMARY KEY (username)
                        )""")
                    
            cursor.execute("""insert into User (username, password, fName, lName, email) 
                        values (%s, %s, %s, %s, %s)""",
                        ("stallylol", "123456", "Stally", "Duan", "user1@gmail.com"))
            cursor.execute("""insert into User (username, password, fName, lName, email) 
                        values (%s, %s, %s, %s, %s)""",
                        ("shiyugun", "abcdef", "Shiyu", "Gao", "user2@gmail.com"))
            cursor.execute("""insert into User (username, password, fName, lName, email) 
                        values (%s, %s, %s, %s, %s)""",
                        ("aspenrocks", "78910", "Aspen", "Forster", "user3@gmail.com"))
            cursor.execute("""insert into User (username, password, fName, lName, email) 
                        values (%s, %s, %s, %s, %s)""",
                        ("toBeDeleted", "wtfwtf", "Dummy", "Value", "user4@gmail.com"))
        self.connection.commit()


    def tearDown(self):
        try:
            self.connection.close()
        except Exception as e:
            print(str(e))
    
    def countUsers(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT count(*) from User;")
            return cursor.fetchone()[0]

    def userExists(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM User WHERE username = %s", (username,))
            return cursor.fetchone()[0] == 1
    
    def test_getAll(self):
        
        with UserManager(self.connection) as db:
            # confirm that number of records returned is same as number of 
            # records in test_database
            self.assertTrue(self.countUsers() == len(db.getAll()))
    
    def test_getItem(self):
        #log = logging.getLogger("TestLog for test_getItem()")
        with UserManager(self.connection) as db:
            # confirm true when user exists
            #log.debug("output from db.getItem(aspenrocks): " + str(db.getItem("aspenrocks")))
            self.assertTrue(db.getItem("aspenrocks")[0] == 'aspenrocks')
            # confirm that getItem() returns none when username not in db
            #log.debug("output from db.getItem(34): " + str(db.getItem("34")))
            self.assertIsNone(db.getItem("34"))
        
    
    def test_InsertItem(self):
        count = self.countUsers()
        with UserManager(self.connection) as db:
            #confirm multiple users can be added 
            self.assertTrue(db.insertItem("papakase", "xxxyyy", "kaspian", "fitz", "user4@gmail.com"))
            self.assertTrue(count + 1 == self.countUsers())
            self.assertTrue(db.insertItem("ranoutofpeople", "666999", "Joan", "Arc", "user5@gmail.com"))
            self.assertTrue(count + 2 == self.countUsers())
            #confirm repeat username is rejected due to primary key constraint
            self.assertFalse(db.insertItem("papakase", "element", "kaspian", "fitz", "user4@gmail.com"))
             #confirm null values are rejected due to not null constraint
            self.assertFalse(db.insertItem("papakase", "element", "kaspian", "fitz", None))
    
    def test_UpdateItem(self):
        log = logging.getLogger("TestLog for test_updateItem()")
        with UserManager(self.connection) as db:
            #update password
            #log.debug("output from db.updateItem(stallylol): " + str(db.updateItem('stallylol', '111213')))
            log.debug('output from getItem(stallylol) post password change: ' + str(db.getItem('stallylol')))
            self.assertTrue(db.updateItem("stallylol", "111213"))
            #fail update becuase username does not exist
            self.assertFalse(db.updateItem("someoneelse", "wrong"))

    def test_deleteItem(self):
        if self.connection is None:
            self.connect()
        count = self.countUsers()
        username = "toBeDeleted"
        with UserManager(self.connection) as db:
            #check user exists first
            self.assertTrue(self.userExists(username))
            # delete user
            db.deleteItem(username)
            #check user does not exist anymore
            self.assertFalse(self.userExists(username))
            # check number of rows reflect deleted user
            self.assertTrue(self.countUsers() == count - 1)
    
def suite ():
    suite = unittest.TestSuite()
    suite.addTest(TestUserManager('test_getAll'))
    suite.addTest(TestUserManager('test_getItem'))
    suite.addTest(TestUserManager('test_InsertItem'))
    suite.addTest(TestUserManager('test_UpdateItem'))
    suite.addTest(TestUserManager('test_deleteItem'))
    
    return suite

      
if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    runner = unittest.TextTestRunner()
    runner.run(suite())




