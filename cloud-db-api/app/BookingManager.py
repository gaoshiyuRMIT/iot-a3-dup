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
        '''
        :param dict row: a row (dict) of booking fetched from database
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
        res = super().getMany(filt)
        res = [BookingManager.tranformDateTime(row) for row in res]
        return res

    def updateOne(self, booking_id, newBookingVal: dict) -> bool:
        return super().updateOne(booking_id, newBookingVal)

    def addOne(self, newBookingVal: dict):
        return super().addOne(newBookingVal)

    def getOne(self, booking_id) -> dict:
        data = super().getOne(booking_id)
        return BookingManager.tranformDateTime(data) if data is not None else None
