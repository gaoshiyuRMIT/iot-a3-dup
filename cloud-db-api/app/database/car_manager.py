#!/usr/bin/python3
import pymysql as p
from db_manager import DBManager
from db_exception import DBException


"""The CarManager class completes all operations regarding the Car table
in the pi-database. It is derived from DBManager."""


class CarManager(DBManager):

    TABLE = "Car"

    def __init__(self, connection=None):
        super().__init__(connection)

    """CreateTable creates the Car table and commits it to database, if
    it doesnt exist already. """
    def createTable(self):
        # cost_hour has max 6 digits, max 2 to right of decimal pt
        # latitude and longitude have max 38 digits, 20 to right of
        # decimal pt, can be null.
        try:
            self.connect()      # connect() method inherited from DBManager
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Car(
                    car_id INT not null auto_increment,
                    year INT not null,
                    car_model VARCHAR(32) not null,
                    body_type VARCHAR(32) not null,
                    num_seats INT not null,
                    car_colour VARCHAR(32) not null,
                    cost_hour  DECIMAL(6,2) not null,
                    latitude DECIMAL(38, 20),
                    longitude DECIMAL(38, 20),
                    car_status VARCHAR(32) not null,
                    PRIMARY KEY (car_id)
                    )""")
            self.connection.commit()    # commit to finalise change to database
        except p.Error as e:    # all errors related to db functioning
            self.connection.rollback()  # reverse any changes
            raise DBException('DB Error while creating Car table',
                              e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            self.connection.rollback()  # reverse any changes
            raise DBException('NON-DB Error while creating Car table',
                              str(e.args))

    """insertItem() take most attributes of the Car table as arguments,
    except 'car_id' and status (which are automatically generated), and
    inserts a new car record/row into the Car table. 'Latitude' and
    'longtitude' do not have to be supplied and will be null if not.
    'Status' is automatically assigned to 'available'.
    Returns True if row has been successfuly inserted. """
    def insertItem(self, year, model, bodyType, seats, colour, cost,
                   latitude=None, longitude=None):
        car_status = 'available'
        if latitude is not None:
            # Case 1: all car attributes supplied
            try:
                sql = "INSERT INTO " + self.TABLE + """ (year, car_model,
                    body_type, num_seats, car_colour, cost_hour, latitude,
                    longitude, car_status) values
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                with self.connection.cursor() as cursor:
                    done = cursor.execute(
                            sql, (year, model, bodyType, seats, colour,
                                  cost, latitude, longitude, car_status))
                    self.connection.commit()
                return done == 1
            except p.Error as e:    # all errors related to db functioning
                self.connection.rollback()  # reverse any changes
                raise DBException('DB Error while inserting complete record into Car',
                                  e.args[1], e.args[0])
            except Exception as e:   # catch any other types of errors
                self.connection.rollback()  # reverse any changes
                raise DBException('NON-DB Error while inserting complete Car record',
                                  str(e.args)
        elif latitude is None:
            # Case 2: latitude and longtitude not supplied
            sql = "INSERT INTO " + self.TABLE + """ (year, car_model,
                    body_type, num_seats, car_colour, cost_hour, car_status)
                    values (%s, %s, %s, %s, %s, %s, %s)"""
            try:
                with self.connection.cursor() as cursor:
                    done = cursor.execute(sql, (year, model,
                            bodyType, seats, colour, cost, car_status,))
                    self.connection.commit()
                return done == 1
            except p.Error as e:    # all errors related to db functioning
                self.connection.rollback()  # reverse any changes
                raise DBException('DB Error while inserting new Car record',
                                  e.args[1], e.args[0])
            except Exception as e:   # catch any other types of errors
                self.connection.rollback()  # reverse any changes
                raise DBException(
                    'NON-DB Error while inserting new Car record',
                    str(e.args))

    """getItem() returns a specific row matching passed argument
    car_id. If the car_id is not in the table returns an empty tuple."""
    def getItem(self, car_id):
        sql = "SELECT * FROM " + self.TABLE + " WHERE car_id = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, car_id)
                resultall = cursor.fetchall() #must be stored in a variable as the finally claues will execute prior to the return stattement
                return resultall
        except p.Error as e:    # all errors related to db functioning
                raise DBException('DB Error while getting a Car record',
                                  e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
                raise DBException(
                    'NON-DB Error while getting a Car record',
                    str(e.args))

    """getAll() returns all the records in the Car table as a
    set/tuple of tuples."""
    def getAll(self):
        sql = "SELECT * FROM " + self.TABLE
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                resultall = cursor.fetchall() #must be stored in a variable as the finally claues will execute prior to the return stattement
                return resultall
        except p.Error as e:    # all errors related to db functioning
                raise DBException('DB Error while getting all Car records',
                                  e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
                raise DBException('NON-DB Error while getting all Car records',
                                  str(e.args))

    """getAllAvailable() returns all cars where 'car_status' is 'available'"""
    def getAllAvailable(self):
        car_status = 'available'
        sql = "SELECT * FROM " + self.TABLE + """ WHERE car_status = %s """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (car_status,))
                fetchall = cursor.fetchall()
            return fetchall
        except p.Error as e:    # all errors related to db functioning
                raise DBException('DB Error while getting all Car records',
                                  e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
                raise DBException('NON-DB Error while getting all Car records',
                                  str(e.args))

    """getLocation returns rows containing car_id, latitutde and longtitude
    columns. If 'car_id' argument is passed, returns any record with matching
    car_id."""
    def getLocation(self, car_id=None):
        # case 1: no car_id supplied
        if car_id is None:
            sql = "SELECT car_id, latitude, longtitude FROM " + self.TABLE
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(sql)
                    resultall = cursor.fetchall() #must be stored in a variable as the finally claues will execute prior to the return stattement
                    return resultall
            except p.Error as e:    # all errors related to db functioning
                raise DBException('DB Error while getting all Car locations',
                                  e.args[1], e.args[0])
            except Exception as e:   # catch any other types of errors
                raise DBException('NON-DB Error while getting all Car locations',
                                  str(e.args))
        # case 2: car_id supplied
        else:
            sql = "SELECT car_id, latitude, longtitude FROM " + self.TABLE \
                  + " WHERE car_id = %s"
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(sql, car_id)
                    resultall = cursor.fetchall() 
                    return resultall
            except p.Error as e:    # all errors related to db functioning
                raise DBException('DB Error while getting all Car locations',
                                  e.args[1], e.args[0])
            except Exception as e:   # catch any other types of errors
                raise DBException('NON-DB Error while getting all Car locations',
                                  str(e.args))

    """getAllYear returns all rows that match the passed year variable,
    and status = 'available'. If a status argument is passed, that will
    be used instead."""
    def getAllYear(self, year, car_status=None):
        if car_status is None:
            car_status = 'available'
        sql = "SELECT * FROM " + self.TABLE + """ WHERE year = %s 
                AND car_status = %s"""
        try:
            return getAllAttribute(sql, year, car_status)
        except p.Error as e:    # all errors related to db functioning
            raise DBException(
                'DB Error while getting Car records according to year',
                e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            raise DBException(
                'NON-DB Error while getting Car records according to year',
                str(e.args))

    """getAllModel returns all rows that match the passed model variable,
    and status = 'available'. If a status argument is passed that will
    be used instead."""
    def getAllModel(self, model, status=None):
        if status is None:
            car_status = 'available'
        sql = "SELECT * FROM " + self.TABLE + """WHERE car_model = %s 
                AND car_status= %s"""
        try:
             return getAllAttribute(sql, model, car_status)
        except p.Error as e:    # all errors related to db functioning
            raise DBException(
                'DB Error while getting Car records according to model',
                e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            raise DBException(
                'NON-DB Error while getting Car records according to model',
                str(e.args))

    """getAllBody returns all rows that match the passed car_body variable,
    and status = 'available'. If a status argument is passed that will
    be used instead."""
    def getAllBody(self, body_type, status=None):
        if status is None:
            car_status = 'available'
        sql = "SELECT * FROM " + self.TABLE + """ WHERE body_type = %s 
                AND car_status = %s"""
        try:
            return getAllAttribute(sql, body_type, car_status)
        except p.Error as e:    # all errors related to db functioning
            raise DBException(
                'DB Error while getting Car records according to car_body',
                e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            raise DBException(
                'NON-DB Error while getting Car records according to car_body',
                str(e.args))

    """getAllSeats returns all rows that match the passed seats variable,
    and status = 'available'. If a status argument is passed that will
    be used instead."""
    def getAllSeats(self, seats, status=None):
        if status is None:
            car_status = 'available'
        sql = "SELECT * FROM " + self.TABLE + """ WHERE num_seats = %d 
                AND car_status = %s"""
        try:
            return getAllAttribute(sql, seats, car_status)
        except p.Error as e:    # all errors related to db functioning
            raise DBException(
                'DB Error while getting Car records according to seats number',
                e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            raise DBException(
                'NON-DB Error while getting Car records according to seat number',
                str(e.args))

    """getAllColour returns all rows that match the passed colour variable,
    and status = 'available'. If a status argument is passed that will
    be used instead."""
    def getAllColour(self, colour, status=None):
        if status is None:
            car_status = 'available'
        sql = "SELECT * FROM " + self.TABLE + """ WHERE car_colour = %s 
                AND car_status = %s"""
        try:
            return getAllAttribute(sql, colour, car_status)
        except p.Error as e:    # all errors related to db functioning
            raise DBException(
                'DB Error while getting Car records according to colour',
                e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            raise DBException(
                'NON-DB Error while getting Car records according to colour',
                str(e.args))

    """getAllCost returns all rows that match the passed cost variable,
    and status = 'available'. If a status argument is passed that will
    be used instead."""
    def getAllCost(self, cost, status=None):
        if status is None:
            car_status = 'available'
        sql = "SELECT * FROM " + self.TABLE + """ WHERE cost = %s 
                AND car_status = %s"""
        try:
            return getAllAttribute(sql, cost, car_status)
        except p.Error as e:    # all errors related to db functioning
            raise DBException(
                'DB Error while getting Car records according to cost',
                e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            raise DBException(
                'NON-DB Error while getting Car records according to cost',
                str(e.args))

    """getAllAttribute is a helper method that takes a parameterised sql
    statement and variables and executes it against the Car Table,
    returning all rows that match.
    It is for use in the searching functionality of the app and therefore
    takes car_status as an argument as well."""
    def getAllAttribute(self, sql_statement, variable, car_status):
        if self.connection is None:
            self.connection = self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(sql_statement, (variable, car_status,))
            return cursor.fetchall()

    """updateItem updates the latitude and longtitude of a car row,
    based on passed values, according to car_id. returns True if update
    successful. """
    def updateItem(self, car_id, latitude, longitude):
        sql = "UPDATE " + self.TABLE + """ SET latitude = %s, longitude = %s 
                WHERE car_id = %s"""
        try:
            with self.connection.cursor() as cursor:
                done = cursor.execute(sql, (latitude, longitude, car_id,))
                self.connection.commit()
            return done == 1
        except p.Error as e:    # all errors related to db functioning
            self.connection.rollback()
            raise DBException(
                'DB Error while updating lat and long for a Car',
                e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            self.connection.rollback()
            raise DBException(
                'NON-DB Error while updating lat and long for a Car',
                str(e.args))


    """deleteItem takes a car_id as argument and deletes any row with
    matching id. The booking table will also set the car_id to null, if
    it exists in that table, on deletion here."""
    def deleteItem(self, car_id):
        sql = "DELETE FROM " + self.TABLE + " WHERE car_id = %s"
        try:
            with self.connection.cursor() as cursor:
                done = cursor.execute(sql, (car_id,))
                self.connection.commit()
            return done == 1
        except p.Error as e:    # all errors related to db functioning
            self.connection.rollback()
            raise DBException(
                'DB Error while deleting Car record',
                e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            self.connection.rollback()
            raise DBException(
                'NON-DB Error while deleting car record',
                str(e.args))

    """BookCar changes car_status of car matching passed car_id argument to
    'booked'. Returns true of action completed false if not. """
    def bookCar(self, car_id):
        car_status = 'booked'
        sql = "UPDATE " + self.TABLE + " SET car_status = %s WHERE car_id = %s"
        try:
            with self.connection.cursor() as cursor:
                done = cursor.execute(sql, (car_status, car_id,))
                self.connection.commit()
            return done == 1
        except p.Error as e:    # all errors related to db functioning
            self.connection.rollback()
            raise DBException(
                'DB Error while changing Car status to booked',
                e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            self.connection.rollback()
            raise DBException(
                'NON-DB Error changing Car status to booked',
                str(e.args))

    def returnCar(self, car_id):
        car_status = 'available'
        sql = "UPDATE " + self.TABLE + " SET car_status = %s WHERE car_id = %s"
        try:
            with self.connection.cursor() as cursor:
                done = cursor.execute(sql, (car_status, car_id,))
                self.connection.commit()
            return done == 1
        except p.Error as e:    # all errors related to db functioning
            self.connection.rollback()
            raise DBException(
                'DB Error while changing Car status to available',
                e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            self.connection.rollback()
            raise DBException(
                'NON-DB Error changing Car status to available',
                str(e.args))

    def useCar(self, car_id):
        car_status = 'inProgress'
        sql = "UPDATE " + self.TABLE + " SET car_status = %s WHERE car_id = %s"
        try:
            with self.connection.cursor() as cursor:
                done = cursor.execute(sql, (car_status, car_id,))
                self.connection.commit()
            return done == 1
        except p.Error as e:    # all errors related to db functioning
            self.connection.rollback()
            raise DBException(
                'DB Error while changing Car status to inProgress',
                e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            self.connection.rollback()
            raise DBException(
                'NON-DB Error changing Car status to inProgress',
                str(e.args))