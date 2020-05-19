from .BaseService import BaseService

class BookingService(BaseService):
    def getBookingsForUser(self, username: str) -> list:
        url = "/bookings/search"
        data = {"username": username}
        bookings = self.post(url, data)
        bookings.sort(key=BookingService.bookingsSortKey)
        return bookings

    def getBookings(self, filt: dict, sortKey = None) -> list:
        url = "/bookings/search"
        bookings = self.post(url, filt)
        if sortKey:
            bookings.sort(sortKey)
        return bookings

    def findConflicts(self, car_id, date_booking, date_return) -> bool:
        filter1 = [
            {"date_booking": [date_booking, date_return]},
            {"date_return": [date_booking, date_return]}
        ]
        filter2 = [
            {"status": "booked"}, 
            {"status": "inProgress"}
        ]
        d3 = {"car_id": car_id}
        for d1 in filter1:
            for d2 in filter2:
                bookings = self.getBookings({**d1, **d2, **d3})
                if len(bookings) > 0:
                    return True
        return False

    def getBooking(self, booking_id: int) -> dict:
        url = "/bookings/{}".format(booking_id)
        return self.get(url)

    def addBooking(self, booking: dict):
        '''
        :param dict booking: a dictionary representing the new booking
        :return: booking_id of the new booking
        :rtype: int
        '''
        url = "/bookings/add"
        return self.post(url, booking)["booking_id"]

    def updateBooking(self, booking_id, updateDict: dict):
        '''
        :param dict updateDict: a dictionary containing pairs of key & value to update that key with
        '''
        url = "/bookings/{}/update".format(booking_id)
        return self.put(url, updateDict)["success"]


    @staticmethod
    def bookingsSortKey(booking) -> tuple:
        '''
        Sort bookings first by status (active ones first),
        and then by booking_id.
        '''
        statusKey = 0
        if booking['status'] in ("finished", "cancelled"):
            statusKey = 1
        return (statusKey, booking['booking_id'])
