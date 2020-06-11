from datetime import date, datetime, timedelta
from .base_service import BaseService

class BookingService(BaseService):
    DATE_FMT = "%Y-%m-%d"

    def get_bookings_for_car(self, car_id: int):
        url = f"/bookings/search"
        data = {"car_id": car_id}
        bookings = self.post(url, data)
        return bookings

    def search_bookings(self, query: dict):
        url = f"/bookings/search"
        bookings = self.post(url, query)
        return bookings

    def transform_date(self, booking: dict):
        booking["date_booking"] = datetime.strptime(booking["date_booking"], self.DATE_FMT).date()
        booking["date_return"] = datetime.strptime(booking["date_return"], self.DATE_FMT).date()

    def transform_time(self, booking: dict):
        for k in ("time_booking", "time_return"):
            time_s = booking[k]
            h, m, s = [int(s_) for s_ in time_s.split(":")]
            booking[k] = timedelta(hours=h, minutes=m, seconds=s)
        return booking

    def gen_date_str(self, date_):
        return date.strftime(date_, self.DATE_FMT)

    def get_all_with_cars(self):
        url = f"/bookings/all_with_cars"
        return self.get(url, {})