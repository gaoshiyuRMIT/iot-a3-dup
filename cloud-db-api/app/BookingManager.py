import pymysql as _p
import datetime
from .DBManager import DBManager


class BookingManager(DBManager):
    FIELDS = ["booking_id", "username", "car_id", "date_booking", "time_booking", 
                "date_return", "time_return", "status"]
    TABLE_NAME = "Booking"

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
        if (list(newBookingVal.keys()) != ["status"]):
            raise NotImplementedError
        status = newBookingVal["status"]
        
        if (status == "finished" or status == "cancelled"):
            sql = "UPDATE " + self.TABLE_NAME + " SET status = %s WHERE booking_id = %s"
            success = False
            conn = self.conn
            try:
                with conn.cursor() as cursor:
                    done = cursor.execute(sql, (status, booking_id,))
                    self.conn.commit() 
                success = done == 1
            except (_p.OperationalError, _p.InternalError, _p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
                conn.rollback()
                raise
            except _p.ProgrammingError:
            #error related to sql syntax etc
                conn.rollback()
                raise
            except _p.DataError:
            # error related to the datatypes passed in not being valid/conflict
                conn.rollback()
                raise
            except:
            # unkown error
                conn.rollback()
                raise
        else:
            raise NotImplementedError
        return success

    def addOne(self, newBookingVal: dict):
        sql = "insert into {} (".format(self.TABLE_NAME)
        names = []
        vals = []
        for k,v in newBookingVal.items():
            names.append(k)
            vals.append(v)
        sql += ", ".join(names) + ") values ("
        sql += ", ".join(["%s"] * len(vals)) + ")"
        bk_id = None
        conn = self.conn
        try:
            with conn.cursor() as cur:
                cur.execute(sql, vals)
            conn.commit()
            with conn.cursor() as cur:
                cur.execute("select last_insert_id()")
            bk_id = cur.fetchone()[0]
        except:
            conn.rollback()
            raise
        return bk_id

    def getOne(self, booking_id) -> dict:
        sql = "SELECT * FROM " + self.TABLE_NAME + " WHERE booking_id = %s"
        data = None
        conn = self.conn
        try:
            with self.getCursor(conn) as cursor:
                cursor.execute(sql, (booking_id,))
                data = cursor.fetchone()
        except (_p.OperationalError, _p.InternalError, _p.NotSupportedError): #errors related to db functioning
            # "Internal Database error"
            raise
        except _p.ProgrammingError:
            #error rrelated to sql syntax etc
            raise
        except:
            # unkown error
            raise
        return BookingManager.tranformDateTime(data) if data is not None else None
