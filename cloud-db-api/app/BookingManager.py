from .DBManager import DBManager


class BookingManager(DBManager):
    FIELDS = ["bookingNo", "userId", "carId", "status", "datetime"]
    TABLE_NAME = "booking"

    def getMany(self, filt: dict) -> list:
        return []

    def updateOne(self, bookingNo, newBookingVal: dict) -> bool:
        return True

    def addOne(self, newBookingVal: dict):
        # returns booking No
        return 1

    def getOne(self, id) -> dict:
        raise NotImplementedError