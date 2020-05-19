#!/usr/bin/python3
import pymysql as p
from db_manager import DBManager
from db_exception import DBException

class BookingManager(DBManager):
    # status = booked, finished, cancelled
    TABLE = "Booking"

    def __init__(self, connection=None):
        super().__init__(connection)

    """CreateTable creates the Booking table and commits to database if
    it doesn't exist already"""
    def createTable(self):
        # date format is 'yyyy-mm-dd'
        # time format is 'HH:MM:SS' OR 'HHMMSS'
        # on delete/update cascade means that if a foriegn key is deleted
        # from the parent table, any corresponding records in this table
        # will also be deleted. On delete set null means that if this
        # table has records with the corresponding foreign key,
        # the values for that key will be made null.
        try:
            with self.connection.cursor() as cursor:
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
            self.connection.commit()    # commit the change to the database
        except p.Error as e:            # errors related to db functioning
            self.connection.rollback()  # reverse any changes
            raise DBException('DB Error while creating Booking table',
                              e.args[1], e.args[0])
        except Exception as e:   # catch any other types of errors
            raise DBException('NON-DB Error while creating Booking table',
                              str(e.args))

    """getAll() returns records based on argument supplied. If no arg,
    returns all the records in the Booking table as a set/tuple of
    tuples. When username is supplied, returns all records
    matching that username. If username AND status are supplied, returns
    all bookings matching those parameters."""
    def getAll(self, username=None, status=None):
        try:
            if username is None and status is None:
                # return contents of table
                sql = "SELECT * FROM " + self.TABLE
                with self.connection.cursor() as cursor:
                    cursor.execute(sql)
                    fetchall = cursor.fetchall()
                return fetchall

            elif status is None:
                # username supplied - return rows matching username
                sql = "SELECT * FROM " + self.TABLE + " WHERE username = %s"
                with self.connection.cursor() as cursor:
                    cursor.execute(sql, (username,))
                    fetchall = cursor.fetchall()
                return fetchall

            else:
                # get user's bookings matching status argument supplied
                sql = "SELECT * FROM " + self.TABLE + """ WHERE
                    username = %s AND status = %s"""
                with self.connection.cursor() as cursor:
                    cursor.execute(sql, (username, status,))
                    fetchall = cursor.fetchall()
                return fetchall

        except p.Error as e:            # errors related to db functioning
            raise DBException('DB Error while getting booking information',
                              e.args[1], e.args[0])
        except Exception as e:          # any other type of errors
            raise DBException(
                'NON-DB Error while getting Booking table information',
                str(e.args))

    """"getItem(booking_id) returns a specific row in the form of a tuple
    matching passed argument 'booking_id'. If the booking_id is not
    in the table, returns none."""
    def getItem(self, booking_id):
        sql = "SELECT * FROM " + self.TABLE + " WHERE booking_id = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (booking_id,))
                fetchone = cursor.fetchone()
            return fetchone
        except p.Error as e:            # errors related to db functioning
            raise DBException('DB Error retrieving a Booking table row',
                              e.args[1], e.args[0])
        except Exception as e:          # any other type of errors
            raise DBException('NON-DB Error retrieving Booking table row',
                              str(e.args))

    """insertItem() takes as arguments most elements/columns of the 
    Booking table, and inserts a new record/row into the table.
    'booking_id' is automatically generated, and 'status' is
    automatically set to 'booked' as a new booking is the only time a 
    new record will be insterted into this table.
    Returns True if row  successfully inserted."""
    def insertItem(self, username, car_id, date_booking, time_booking,
                   date_return, time_return):
        status = "booked"
        sql = "INSERT INTO " + self.TABLE + """ (username, car_id, 
                date_booking, time_booking, date_return, time_return,
                status) values (%s, %s, %s, %s, %s, %s, %s)"""
        try:
            with self.connection.cursor() as cursor:
                done = cursor.execute(
                    sql, (username, car_id, date_booking, time_booking,
                          date_return, time_return, status,))
                self.connection.commit()
            return done == 1
        except p.Error as e:         # errors related to db functioning
            self.connection.rollback()
            raise DBException('DB Error inserting new Booking table record',
                              e.args[1], e.args[0])
        except Exception as e:       # any other type of errors
            self.connection.rollback()
            raise DBException('NON-DB Error inserting new Booking record',
                              str(e.args))

    """updateItem() updates the status of a booking to 'finished' or
    'cancelled' (if the supplied 'booking_id' is present in the table).
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
            except p.Error as e:         # errors related to db functioning
                self.connection.rollback()
                raise DBException(
                    'DB Error updating status of a Booking record',
                    e.args[1], e.args[0])
            except Exception as e:       # any other type of errors
                self.connection.rollback()
                raise DBException(
                    'NON-DB Error updating status of a Booking record',
                    str(e.args))

