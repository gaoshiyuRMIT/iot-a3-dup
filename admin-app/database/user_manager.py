#!/usr/bin/python3
import pymysql as p
from db_manager import DBManager
from db_exception import DBException

"""The UserManager class completes all operations regarding the User
table in the pi-database. It is derived from DBManager."""


class UserManager(DBManager):

    TABLE = "User"

    def __init__(self, connection=None):
        super().__init__(connection)

    """CreateTable creates the User table and commits to database, if
    it doesn't exist already"""
    def createTable(self):
        try:
            # 'with ... as ...' automatically closes cursor on exit
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS User (
                    username VARCHAR(32) not null,
                    password VARCHAR(255) not null,
                    fName VARCHAR(32) not null,
                    lName VARCHAR(32) not null,
                    email VARCHAR(255) not null,
                    CONSTRAINT PK_User PRIMARY KEY (username)
                    )""")
            self.connection.commit()     # commit the change to database
        except p.Error as e:    # all errors related to db functioning
            self.connection.rollback()  # reverse any changes
            raise DBException('DB Error while creating User table',
                              e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            raise DBException('NON-DB Error while creating User table',
                              str(e.args))

    """getAll() returns all the records in the User table as a
    set/tuple of tuples"""
    def getAll(self):
        sql = "SELECT * FROM " + self.TABLE
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except p.Error as e:
            raise DBException('DB Error retrieving all Users',
                              e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            raise DBException('NON_DB Error retrieving all Users', str(e.args))

    """"getItem() returns a specific row matching passed argument
    'username'. If the username is not in the table, returns empty tuple"""
    def getItem(self, username):
        sql = "SELECT * FROM " + self.TABLE + " WHERE username = %s"
        try:
            if self.connection is None:
                self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (username,))
                return cursor.fetchone()
        except p.Error as e:
            raise DBException(
                'DB Error retrieving User information (by username)',
                e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            raise DBException(
                'NON-DB Error retrieving User information (by username)',
                str(e.args))

    """insertItem() takes all elements of the User table as arguments
    and inserts a new User record/row into the User table. The password
    argument is expected to be a hash of the password entered by user.
    Returns true if insertion is successful."""
    def insertItem(self, username, password, fName, lName, email):
        sql = "INSERT INTO " + self.TABLE + """ (username, password,
            fName, lName, email) values (%s, %s, %s, %s, %s)"""
        try:
            if self.connection is None:
                self.connect()
            with self.connection.cursor() as cursor:
                done = cursor.execute(
                    sql, (username, password, fName, lName, email,))
                self.connection.commit()
            return done == 1
        except p.Error as e:
            self.connection.rollback()  # reverse any changes
            raise DBException('DB Error inserting new User (into User table)',
                              e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            raise DBException('NON-DB Error inserting new User (into User table)',
                              str(e.args))

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
        except p.Error as e:
            self.connection.rollback()  # reverse any changes
            raise DBException('DB Error updating User password (in User table)',
                              e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            raise DBException('NON-DB Error updating User password (in User table)',
                              str(e.args))

    """DeleteItem deletes a user, identifid via username argument supplied.
    If this user has a booking history, this will also be deleted from
    the Booking table. Returns true if user deleted."""
    def deleteItem(self, username):
        sql = "DELETE FROM " + self.TABLE + " WHERE username = %s"
        try:
            if self.connection is None:
                self.connect()
            with self.connection.cursor() as cursor:
                done = cursor.execute(sql, (username,))
                self.connection.commit() 
            return done == 1
        except p.Error as e:
            self.connection.rollback()  # reverse any changes
            raise DBException('DB Error deleting user', e.args[1], 
                              e.args[0])
        except Exception as e:   # catch any other types of errors
            raise DBException('NON-DB Error deleting user', str(e.args))
