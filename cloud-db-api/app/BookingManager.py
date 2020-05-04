from .DBManager import DBManager


class BookingManager(DBManager):
    FIELDS = ["booking_id", "username", "car_id", "date_booking", "time_booking", 
                "date_return", "time_return", "status"]
    TABLE_NAME = "Booking"

    def getMany(self, filt: dict) -> list:
        return [{
            "booking_id": 1, "username": "Jane Doe", "car_id": 1, "date_booking": "2020-01-01",
            "time_booking": "19:58:02", "date_return": "2020-01-05", "time_return": "11:00:00", 
            "status": "available" 
        }]

    def updateOne(self, bookingNo, newBookingVal: dict) -> bool:
        return True

    def addOne(self, newBookingVal: dict):
        # returns booking No
        return 1

    def getOne(self, id) -> dict:
        raise NotImplementedError