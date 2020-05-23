from .BaseService import BaseService

class BookingService(BaseService):
    def getBookingsForUser(self, username: str) -> list:
        '''get all bookings of a user

        :param str username: username
        :return: a list of dictionaries each representing a booking
        :rtype: list
        '''
        url = "/bookings/search"
        data = {"username": username}
        bookings = self.post(url, data)
        bookings.sort(key=BookingService.bookingsSortKey)
        return bookings

    def getBookings(self, filt: dict, sortKey = None) -> list:
        '''search for bookings using a filter dictionary

        :param dict filt: filter dictionary
        :param function sortKey: sorting key to sort the returned list of bookings, default None (not sorted)
        :return: bookings as a result of the search
        :rtype: list
        '''
        url = "/bookings/search"
        bookings = self.post(url, filt)
        if sortKey:
            bookings.sort(sortKey)
        return bookings

    def findConflicts(self, car_id, date_booking, date_return) -> bool:
        '''find out if there's any active booking of this car that conflict with the supplied booking & return date

        :param int car_id: car ID
        :param str date_booking: start date of booking as an ISO string
        :param str date_return: return date of booking as an ISO string
        :return: whether timetabling conflicts exist
        :rtype: bool
        '''
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
        '''get one booking, providing booking_id

        :param int booking_id: booking ID
        :return: booking data with this id
        :rtype: dict
        '''
        url = "/bookings/{}".format(booking_id)
        return self.get(url)

    def addBooking(self, booking: dict):
        '''add a new booking

        :param dict booking: a dictionary representing the new booking
        :return: booking_id of the new booking
        :rtype: int
        '''
        url = "/bookings/add"
        return self.post(url, booking)["booking_id"]

    def updateBooking(self, booking_id, updateDict: dict):
        '''update a booking, providing bookind_id and the new value

        :param int booking_id: booking ID
        :param dict updateDict: a dictionary containing pairs of (key, new value)
        :return: whether the update is successful
        :rypte: bool
        '''
        url = "/bookings/{}/update".format(booking_id)
        return self.put(url, updateDict)["success"]


    @staticmethod
    def bookingsSortKey(booking) -> tuple:
        '''A function to map a booking to a key used for sorting.
        Sort bookings first by status (active ones first), and then by booking_id.

        :param dict booking: a dictionary representing the booking
        :return: a key to sort the bookings against
        :rtype: tuple
        '''
        statusKey = 0
        if booking['status'] in ("finished", "cancelled"):
            statusKey = 1
        return (statusKey, booking['booking_id'])
