from datetime import date, datetime, timedelta
from .base_service import BaseService

class BookingService(BaseService):
    DATE_FMT = "%Y-%m-%d"

    def get_bookings_for_car(self, car_id: int):
        '''get all bookings given car_id

        :param int car_id: car ID
        :return: all bookings of that car
        :rtype: list
        '''
        url = f"/bookings/search"
        data = {"car_id": car_id}
        bookings = self.post(url, data)
        return bookings

    def search_bookings(self, query: dict):
        '''search for bookings given the query dictionary

        :param dict query: specifies the exact values or range of a key to match
        :return: bookings that satisfy the query
        :rtype: list
        '''
        url = f"/bookings/search"
        bookings = self.post(url, query)
        return bookings

    def transform_date(self, booking: dict):
        '''given a booking, tranform the date_booking and date_return to a datetime.date object

        :param dict booking: key-value map that represents a booking
        '''
        booking["date_booking"] = datetime.strptime(booking["date_booking"], self.DATE_FMT).date()
        booking["date_return"] = datetime.strptime(booking["date_return"], self.DATE_FMT).date()

    def transform_time(self, booking: dict):
        '''given a booking, tranform the time_booking and time_return to datetime.timedelta object

        :param dict booking: key-value map that represents a booking
        :return: booking after time-transformation
        :rtype: dict
        '''
        for k in ("time_booking", "time_return"):
            time_s = booking[k]
            h, m, s = [int(s_) for s_ in time_s.split(":")]
            booking[k] = timedelta(hours=h, minutes=m, seconds=s)
        return booking

    def gen_date_str(self, date_):
        '''generate a string based on an app-specific format (see DATE_FMT) from a datetime.date object

        :param datetime.date date_: input date
        :return: date string that conforms to the app-specific format
        :rtype: str
        '''
        return date.strftime(date_, self.DATE_FMT)

    def get_all_with_cars(self):
        '''get bookings along with car info
        
        :rtype: list
        :return: all bookings, together with the car info of each booking
        '''
        url = f"/bookings/all_with_cars"
        return self.get(url, {})