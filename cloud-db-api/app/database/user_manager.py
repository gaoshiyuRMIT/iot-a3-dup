#!/usr/bin/python3
import pymysql as p
from iot.db_manager import DBManager

class UserManager(DBManager):
    TABLE = "User" 
    # Not sure we even need this init
    def __init__(self, connection=None):
        super().__init__(connection)
    
    
    """CreateTable creates the User table and commits to database if
    it doesn't exist already"""
    def createTable(self):
        try:
            with self.connection.cursor() as cursor: #need the cursor to exectue queries 
            #method called execute - use it to pass sql queries here we are creating the database table 
            #NOT SURE PASSWORD NEEDS TO BE UNIQUE
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS User ( 
                    username VARCHAR(32) not null, 
                    password VARCHAR(255) not null unique,
                    fName VARCHAR(32) not null,
                    lName VARCHAR(32) not null,
                    email VARCHAR(255) not null,   
                    CONSTRAINT PK_User PRIMARY KEY (username)
                    )""")
            self.connection.commit() #commit must be used to commit the change (in execute)to the database- python requires it 
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            self.connection.rollback()
        except p.IntegrityError:
            #relational DB integrity error
            self.connection.rollback()
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            #rollback attempted changes
           self.connection.rollback()
           pass
        except p.DatabaseError:
            pass
 
        
    """getAll() returns all the records in the User table as a
    set/tuple of tuples"""
    def getAll(self):
        sql = "SELECT * FROM " + self.TABLE
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                fetachall = cursor.fetchall()
                return fetachall
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except p.DatabaseError:
            pass


    """"getItem() returns a specific row matching passed argument
     username. If the username is not in the table returns an empty tuple"""
    def getItem(self, username):
        sql = "SELECT * FROM " + self.TABLE + " WHERE username = %s"
        try:
            if self.connection is None:
                self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (username,))
                fetchone = cursor.fetchone();
            return fetchone
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except p.DatabaseError:
            pass
    
    """insertItem() takes all elements of the User table as arguments 
    and inserts a new User record/row into the User table. The password 
    argument is expected to be a hash of the password entered by user"""
    def insertItem(self, username, password, fName, lName, email):
        sql = "INSERT INTO " + self.TABLE + """ (username, password, 
                fName, lName, email) values (%s, %s, %s, %s, %s)"""
        try:
            if self.connection is None:
                self.connect()
            with self.connection.cursor() as cursor:
                done =cursor.execute(sql, (username, password, fName, lName, email,))
                self.connection.commit() 
            return done == 1
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            self.connection.rollback()
        except p.ProgrammingError:
            # error related to sql syntax etc
                self.connection.rollback()    # rollback attempted changes
        except p.DatabaseError:
            pass
    
    """updateItem() updates a user password in the User table if the 
    supplied username is present in the table. The password argument 
    is expected to be a hash of the password entered by user. Returns 
    true if update is successful"""
    def updateItem(self, username, password):
        sql = "UPDATE " + self.TABLE + " SET password = (%s) WHERE username = (%s)"
        try:
            if self.connection is None:
                self.connect()
            with self.connection.cursor() as cursor:
                done = cursor.execute(sql, (password, username,))
                self.connection.commit()
            return done == 1
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            self.connection.rollback()
        except p.ProgrammingError:
            # error related to sql syntax etc
            self.connection.rollback()    # rollback attempted changes
        except p.DatabaseError:
            pass

    
    """**deleting a user may create complications for booking table"""
    def deleteItem(self, username):
        sql = "DELETE FROM " + self.TABLE + " WHERE username = %s"
        try:
            if self.connection is None:
                self.connect()
            with self.connection.cursor() as cursor:
                done = cursor.execute(sql, (username,))
                self.connection.commit() 
            return done == 1
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except p.DatabaseError:
            pass
      