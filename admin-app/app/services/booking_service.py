from .base_service import BaseService

class BookingService(BaseService):
    def get_bookings_for_car(self, car_id: int):
        url = f"/bookings/search"
        data = {"car_id": car_id}
        bookings = self.post(url, data)
        return bookings
