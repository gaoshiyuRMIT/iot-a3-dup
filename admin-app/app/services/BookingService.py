from .BaseService import BaseService

class BookingService(BaseService):
    def getBookingsForUser(self, username: str) -> list:
        url = "/bookings/search"
        data = {"username": username}
        bookings = self.post(url, data)
        bookings.sort(key=BookingService.bookingsSortKey)
        return bookings

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
