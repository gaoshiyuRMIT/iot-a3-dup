#!/usr/bin/python3
import pymysql as p
from db_manager import DBManager
from car_manager import CarManager
from user_manager import UserManager

class BookingManager(DBManager):
    #status = booked, finished, cancelled
    TABLE = "Booking"

    # Not sure we even need this init
    def __init__(self, connection=None):
        super().__init__(connection)

    """CreateTable creates the Booking table and commits to database if
    it doesn't exist already"""
    def createTable(self):
        # date format is 'yyyy-mm-dd'
        # time format is 'HH:MM:SS' OR 'HHMMSS'
        # on delete/update cascade means that if a foriegn key is deleted from
        # the parent table, any corresponding records in this table will also be
        # deleted. On delete restrict means that if this table has records with the corresponding
        # foreign key, the parent table record can not be deleted - the action will be rejected
        try:
            with self.connection.cursor() as cursor: #need the cursor to exectue queries 
            #method called execute - use it to pass sql queries here we are creating the database table 
                cursor.execute("""CREATE TABLE IF NOT EXISTS Booking ( 
                                booking_id INT not null AUTO_INCREMENT, 
                                username VARCHAR(32) not null,
                                car_id INT, 
                                date_booking DATE not null,
                                time_booking TIME not null,
                                date_return DATE not null,
                                time_return TIME not null,
                                status VARCHAR(32) not null,
                            
                                PRIMARY KEY (booking_id),
                                INDEX (username),
                                INDEX (car_id),
                            
                                FOREIGN KEY (username)
                                    REFERENCES User(username)
                                    ON UPDATE CASCADE ON DELETE CASCADE,
                            
                                FOREIGN KEY (car_id)
                                    REFERENCES Car(car_id)
                                    ON UPDATE CASCADE ON DELETE SET NULL
                                )""")
            self.connection.commit() #commit must be used to commit the change (in execute)to the database- python requires it 
        except p.ProgrammingError() as e: #bad table name 
            #rollback due to error 
            self.connection.rollback()
        except p.OperationalError() as e:#loss of connection
            pass
        except p.IntegrityError() as e: #errors tht damage integrity of table ie uniquness/foreign keys  
            #rollback due to error 
            self.connection.rollback()
        except p.InternalError() as e: #moduoe based error eg cursor not active
            pass
        except:
            #unknown error
            pass

    """getAll() returns records based on argument supplied. If no arg,
    returns all the records in the Booking table as a set/tuple of 
    tuples. When username is supplied, returns all records
    matching that username. If username AND status are supplied, returns
    all bookings matching those parameters. """
    def getAll(self, username=None, status=None):
        try:
            if username is None and status is None: #return contents of table
                sql = "SELECT * FROM " + self.TABLE
                with self.connection.cursor() as cursor:
                    cursor.execute(sql)
                    fetchall = cursor.fetchall()
                return fetchall

            elif status is None: #username supplied - return rows matching username
                sql = "SELECT * FROM " + self.TABLE + " WHERE username = %s"
                with self.connection.cursor() as cursor:
                    cursor.execute(sql, (username,))
                    fetchall = cursor.fetchall()
                return fetchall

            else:   #username and status have been supplied (eg get all previous bookings, or current bookings)
                sql = "SELECT * FROM " + self.TABLE + """ WHERE username = %s
                               AND status = %s"""
                with self.connection.cursor() as cursor:
                    cursor.execute(sql, (username, status,))
                    fetchall = cursor.fetchall()
                return fetchall
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except:
            #unknown error
            pass
        
    """"getItem(booking_id) returns a specific row matching passed argument
     booking_id. If the booking_id is not in the table returns an empty tuple."""
    def getItem(self, booking_id):
        sql = "SELECT * FROM " + self.TABLE + " WHERE booking_id = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (booking_id,))
                fetchone = cursor.fetchone();
            return fetchone
        except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            pass
        except p.ProgrammingError:
            #error rrelated to sql syntax etc
            pass
        except:
            # unkown error
            pass

    """insertItem() takes all elements of the Booking table (except
    booking_id which is automatically created, and status which is 
    automatically set to booked as this is the only timea new record 
    will be insterted into this table) as arguments 
    and inserts a new Booking record/row into the Booking table.
    Returns True if row updated."""
    def insertItem(self, username, car_id, date_booking, time_booking, 
                   date_return, time_return):
        status = "booked"
        sql = "INSERT INTO " + self.TABLE + """ (username, car_id, 
                date_booking, time_booking, date_return, time_return, 
                status) values (%s, %s, %s, %s, %s, %s, %s)"""
        try:
            
            with self.connection.cursor() as cursor:
                done = cursor.execute(sql,(username, car_id, date_booking, time_booking,
                        date_return, time_return, status,))
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
            # error related to the datatypes passed in not being valid/conflict
            self.connection.rollback()
        except p.IntegrityError:
            # error related tocompromising itegrity of dtatabase eg foreign keys
            self.connetion.rollback()
        except:
            # unkown error
            self.connection.rollback()
            pass
            
    
    """updateItem() updates the status of a booking to "finished" or 
    "cancelled" (if the supplied booking_id is present in the table). 
    The default value of status is "finished", otherwise supplied status 
    arg should = 'cancelled'. Returns true if row updated"""
    def updateItem(self, booking_id, status="finished"):
        # should this function not allow status to be changed from finished to
        # cancelled and vice versa? 
        sql = "UPDATE " + self.TABLE + " SET status = %s WHERE booking_id = %s"

        if (status == "finished" or status == "cancelled"):
            try:
                with self.connection.cursor() as cursor:
                    done = cursor.execute(sql, (status, booking_id,))
                    self.connection.commit() 
                return done == 1
            except (p.OperationalError, p.InternalError, p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
                self.connection.rollback()
            except p.ProgrammingError:
            #error related to sql syntax etc
                self.connection.rollback()
            except p.DataError:
            # error related to the datatypes passed in not being valid/conflict
                self.connection.rollback()
            except:
            # unkown error
                self.connection.rollback()
                
