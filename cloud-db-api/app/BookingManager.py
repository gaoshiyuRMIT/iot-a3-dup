import pymysql as _p
import datetime
from .DBManager import DBManager


class BookingManager(DBManager):
    FIELDS = ["booking_id", "username", "car_id", "date_booking", "time_booking", 
                "date_return", "time_return", "status"]
    TABLE_NAME = "Booking"
    PK = "booking_id"

    @staticmethod
    def tranformDateTime(row):
        '''transform date/time returned from database into ISO strings

        :param dict row: a row (dict) of booking fetched from database
        :return: a dictionary in which all date/time values are transformed
        :rtype: dict
        '''
        bk = {}
        for k,v in row.items():
            if isinstance(v, datetime.date):
                v = v.isoformat()
            elif isinstance(v, datetime.timedelta):
                v = str(v)
            bk[k] = v
        return bk

    def getMany(self, filt: dict) -> list:
        '''get all bookings that satisfy the query condition

        :param dict filt: the query condition
        :return: a list of dictionaries, each representing a booking
        :rtype: list
        '''
        res = super().getMany(filt)
        res = [BookingManager.tranformDateTime(row) for row in res]
        return res

    def updateOne(self, booking_id, newBookingVal: dict) -> bool:
        '''provided booking_id and new values, update a booking

        :param int booking_id: booking ID
        :param dict newBookingVal: a dictionary specifying the fields to update and the values to update them with
        :return: whether a row is updated successfully
        :rtype: bool
        '''
        return super().updateOne(booking_id, newBookingVal)

    def addOne(self, newBookingVal: dict):
        '''add a new booking

        :param dict newBookingVal: with all the fields and values of a booking, except booking_id
        :return: the auto-generated booking_id
        :rtype: int
        '''
        return super().addOne(newBookingVal)

    def getOne(self, booking_id) -> dict:
        '''get a booking by supplying booking_id

        :param int booking_id: booking ID
        :return: the booking data
        :rtype: dict
        '''
        data = super().getOne(booking_id)
        return BookingManager.tranformDateTime(data) if data is not None else None

    def deleteOne(self, booking_id) -> dict:
        '''deleted one booking given booking ID
        '''
        return super().deleteOne(booking_id)