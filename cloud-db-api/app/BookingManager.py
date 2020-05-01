from .DBManager import DBManager


class BookingManager(DBManager):
    FIELDS = ["booking_id", "username", "car_id", "date_booking", "time_booking", 
                "date_return", "time_return", "status"]
    TABLE_NAME = "Booking"

    def getMany(self, filt: dict) -> list:
        return []

    def updateOne(self, bookingNo, newBookingVal: dict) -> bool:
        return True

    def addOne(self, newBookingVal: dict):
        # returns booking No
        return 1

    def getOne(self, id) -> dict:
        raise NotImplementedError