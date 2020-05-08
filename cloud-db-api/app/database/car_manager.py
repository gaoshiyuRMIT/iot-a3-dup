#!/usr/bin/python3
import pymysql as p
from iot.db_manager import DBManager

class CarManager(DBManager):
    TABLE = "Car"

    def __init__(self, connection=None):
        super().__init__(connection)
    
    """CreateTable creates the Car table and commits to database, if
    it doesnt exist already. """
    def createTable(self):
        #cost_hour has max 6 digits, max 2 to right of decimal pt
        #lat and long have max 38 digits, 20 to right of decimal pt, can be null 
        try:
            self.connect()  # connect() method is inherited from DBManager class
            with self.connection.cursor() as cursor: #cursor is necessary to execute quiries
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
            self.connection.commit() #commit must be used to commit the change (in execute)to the database
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
        except:
            #unknown error
            pass 
    
    """insertItem() can take all attributes of the Car table as arguments 
    (except car_id which is automatically populated, and status) and inserts a 
    new car record/row into the Car table. Latitude and longtitude do not have
    to be supplied and will be left null if not. Status automatically available.
    Returns True if row has been successfuly inserted. """
    def insertItem(self, year, model, bodyType, seats, colour, cost, 
                    latitude=None, longitude=None):
        status = 'available'
        # Case 1: all car attributes supplied
        if latitude is not None:
            try:
                sql = "INSERT INTO " + self.TABLE + """ (year, car_model, 
                        body_type, num_seats, car_colour, cost_hour, 
                        latitude, longitude, car_status) values 
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                with self.connection.cursor() as cursor:
                    done = cursor.execute(sql,(year, model, bodyType, 
                            seats, colour, cost, latitude, longitude, status))
                    self.connection.commit()
                return done == 1
            except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
                self.connection.rollback()
            except p.ProgrammingError:
            # error rrelated to sql syntax etc
                self.connection.rollback()  # rollback attempted changes
            except:
                #unknown error
                pass

        # Case 2: latitude and longtitude not supplied
        else:
            sql = "INSERT INTO " + self.TABLE + """ (year, 
                    car_model, body_type, num_seats, car_colour, 
                    cost_hour, car_status) values 
                    (%s, %s, %s, %s, %s, %s, %s)"""
            try:
                with self.connection.cursor() as cursor:
                    done = cursor.execute(sql, (year, model, 
                            bodyType, seats, colour, cost, status))
                    self.connection.commit() 
                return done == 1
            except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
                self.connection.rollback()
            except p.ProgrammingError:
            # error related to sql syntax etc
                self.connection.rollback()    # rollback attempted changes
            except:
                pass # unkown error type

    """getItem() returns a specific row matching passed argument
    car_id. If the car_id is not in the table returns an empty tuple"""
    def getItem(self, car_id):
        sql = "SELECT * FROM " + car.TABLE + " WHERE car_id = %s"
        try:
            return getAllAttribute(sql, car_id, car_status)

        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except:
            pass # unkown error type

    """getAll() returns all the records in the Car table as a
    set/tuple of tuples."""
    def getAll(self):
        sql = "SELECT * FROM " + self.TABLE
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                resultall = cursor.fetchall() #must be stored in a variable as the finally claues will execute prior to the return stattement
                return resultall
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except:
            pass # unkown error type
            

    """getAllAvailable() returns all cars that are not curently booked"""
    def getAllAvailable(self):
        # get all cars which exist, if they are available (status != booked) 
        #sql = """"SELECT * FROM Car LEFT JOIN Booking 
        #        ON Car.car_id = Booking.car_id 
        #        WHERE Booking.status != %s"""
        sql = "SELECT * FROM " + self.TABLE + """ WHERE car_status = %s """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, ("available"))
                fetchall = cursor.fetchall()
            return fetchall
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except:
            pass # unkown error type
    
    """getLocation returns rows containing car_id, latitutde and longtitude
    details. If car_id argument is passed, returns any matching car."""
    def getLocation(self, car_id=None):
        # case 1: no car_id supplied
        if car_id is None:
            sql = "SELECT car_id, latitude, longtitude FROM " + self.TABLE
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(sql)
                    resultall = cursor.fetchall() #must be stored in a variable as the finally claues will execute prior to the return stattement
                    return resultall
            except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
                # "Internal Database error"
                pass
            except p.ProgrammingError:
                #error rrelated to sql syntax etc
                pass
            except:
                pass    # unkown error type
        # case 2: car_id supplied
        else:
            sql = "SELECT car_id, latitude, longtitude FROM " + self.TABLE + " WHERE car_id = %s"
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(sql, car_id)
                    resultall = cursor.fetchall() #must be stored in a variable as the finally claues will execute prior to the return stattement
                    return resultall
            except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
                # "Internal Database error"
                pass
            except p.ProgrammingError:
                #error rrelated to sql syntax etc
                pass
            except:
                pass    # unkown error type

    """getAllYear returns all rows that match the passed year variable, 
    and status = 'available'. If a status argument is passed that will
    be used instead. """
    def getAllYear(self, year, car_status=None):
        if car_status is None:
            car_status = 'available'

        sql = "SELECT * FROM " + self.TABLE + " WHERE year = %s AND car_status = %s"
        try:
            return getAllAttribute(sql, year, car_status)

        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except:
            pass # unkown error type
    
    """getAllModel returns all rows that match the passed model variable, 
    and status = 'available'. If a status argument is passed that will
    be used instead."""
    def getAllModel(self, model, status=None):
        if status is None:
            car_status = 'available'
        sql = "SELECT * FROM " + self.TABLE + " WHERE car_model = %s AND car_status= %s"
        try:
             return getAllAttribute(sql, model, car_status)

        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except:
            pass # unkown error type
   
    """getAllBody returns all rows that match the passed car_body variable, 
    and status = 'available'. If a status argument is passed that will
    be used instead."""
    def getAllBody(self, body_type, status=None):
        if status is None:
            car_status = 'available'
        sql = "SELECT * FROM " + self.TABLE + " WHERE body_type = %s AND car_status = %s"
        try:
            return getAllAttribute(sql, body_type, car_status)

        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except:
            pass # unkown error type

    """getAllSeats returns all rows that match the passed seats variable, 
    and status = 'available'. If a status argument is passed that will
    be used instead."""
    def getAllSeats(self, seats, status=None):
        if status is None:
            car_status = 'available'
        sql = "SELECT * FROM " + self.TABLE + "WHERE num_seats = %d AND car_status = %s"
        try:
            return getAllAttribute(sql, seats, car_status)
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except:
            pass # unkown error type

    """getAllColour returns all rows that match the passed colour variable, 
    and status = 'available'. If a status argument is passed that will
    be used instead."""
    def getAllColour(self, colour, status=None):
        if status is None:
            car_status = 'available'
        sql = "SELECT * FROM " + self.TABLE + " WHERE car_colour = %s AND car_status = %s"
        try:
            return getAllAttribute(sql, colour, car_status)

        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error related to sql syntax etc
            pass
        except:
            pass # unkown error type

    """getAllCost returns all rows that match the passed cost variable, 
    and status = 'available'. If a status argument is passed that will
    be used instead."""
    def getAllCost(self, cost, status=None):
        if status is None:
            car_status = 'available'
        sql = "SELECT * FROM " + self.TABLE + " WHERE cost = %s AND car_status = %s"
        try:
            return getAllAttribute(sql, cost, car_status)

        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except:
            pass # unkown error type
          
    """getAllAttribute is a helper method that takes a parameterised sql 
    statement and variables and executes it against the Car Table, 
    returning all rows that match.
    It is for use in the searching functionality of the app and therefore 
    takes car_status as an argument as well."""
    def getAllAttribute(self, sql_statement, variable, car_status):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql_statement, (variable, car_status,))
                return cursor.fetchall()
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except:
            pass # unkown error type
    
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
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            self.connection.rollback()
            pass
        except p.ProgrammingError:
            #error related to sql syntax etc
            self.connection.rollback()
            pass
        except p.DataError:
            #issue related to processing data - problem with input
            self.connection.rollback()
            pass
        except:
            self.connection.rollback()
            pass # unkown error type


    """deleteItem takes a car_id as argument and deletes any row with matching id.
   The booking table will set the car_id to null, if it exists in that table, 
   on deletion here."""
    def deleteItem(self, car_id):
        sql = "DELETE FROM " + self.TABLE + " WHERE car_id = %s"
        try:
            with self.connection.cursor() as cursor:
                done = cursor.execute(sql, (car_id,))
                self.connection.commit()
            return done == 1
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            self.connection.rollback()
            pass
        except p.ProgrammingError:
            #error related to sql syntax etc
            self.connection.rollback()
            pass
        except p.IntegrityError:
            #issue related to integrity of db 
            self.connection.rollback()
            pass
        except:
            self.connection.rollback()
            pass # unkown error type

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
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            self.connection.rollback()
            pass
        except p.ProgrammingError:
            #error related to sql syntax etc
            self.connection.rollback()
            pass
        except p.IntegrityError:
            #issue related to integrity of db 
            self.connection.rollback()
            pass
        except:
            self.connection.rollback()
            pass # unkown error type
    
    def returnCar(self, car_id):
        car_status = 'available'
        sql = "UPDATE " + self.TABLE + " SET car_status = %s WHERE car_id = %s"
        try:
            with self.connection.cursor() as cursor:
                done = cursor.execute(sql, (car_status, car_id,))
                self.connection.commit()
            return done == 1
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            self.connection.rollback()
            pass
        except p.ProgrammingError:
            #error related to sql syntax etc
            self.connection.rollback()
            pass
        except p.IntegrityError:
            #issue related to integrity of db 
            self.connection.rollback()
            pass
        except:
            self.connection.rollback()
            pass # unkown error type
    
    def useCar(self, car_id):
        car_status = 'inProgress'
        sql = "UPDATE " + self.TABLE + " SET car_status = %s WHERE car_id = %s"
        try:
            with self.connection.cursor() as cursor:
                done = cursor.execute(sql, (car_status, car_id,))
                self.connection.commit()
            return done == 1
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            self.connection.rollback()
            pass
        except p.ProgrammingError:
            #error related to sql syntax etc
            self.connection.rollback()
            pass
        except p.IntegrityError:
            #issue related to integrity of db 
            self.connection.rollback()
            pass
        except:
            self.connection.rollback()
            pass # unkown error type
