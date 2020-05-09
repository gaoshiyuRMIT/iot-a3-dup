from datetime import datetime
import pickle
class dataHelper:
    def __init__(self):
        self.time = None
        
    def unlock(self,car_id,user):
        self.time=datetime.now()
        request_type={
            'type' : 'unlock'
        }
        car_data = {
            "status": "booked"
        }    
        book_data={
            "car_id": car_id,
            "date_booking": self.time.strftime('%Y-%m-%d'),
            "time_booking": self.time.strftime('%H-%M-%S'),
            "username": user
        }
        
        data = [request_type,car_data,book_data]
        send_data = pickle.dumps(data)
        return send_data