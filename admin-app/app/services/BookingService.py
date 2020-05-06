from .BaseService import BaseService

class BookingService(BaseService):
    def getBookingsForUser(self, username: str) -> list:
        url = "/bookings/search"
        params = {"username": username}
        bookings = self.get(url, params)
        bookings.sort(key=BookingService.bookingsSortKey)
        return bookings

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
