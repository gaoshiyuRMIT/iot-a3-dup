from datetime import datetime
import json
from location_monitor import create_location

class dataHelper:
    def __init__(self):
        self.time = None
        
    def login(self, username, password):
        """gnerate the login data for ap, ap send these data to the server when the user want login"""
        data={
            'type' : 'login',
            "username": username, 
            "password": password
        }
          
        send_data = json.dumps(data)
        data = send_data.encode('utf-8')
        return data
    
        
    def search_booking(self,user):
        """gnerate the search booking data for ap, it will show all the booked status booking of the user """
        self.time=datetime.now()
        data={
            'type' : 'search_booking',
            "username": user
            }
            
        send_data = json.dumps(data)
        data = send_data.encode('utf-8')
        return data
    
    def search_inprogress(self,user):
        """gnerate the search booking data for ap, it will show all the inProgress status booking of the user """
        self.time=datetime.now()
        data={
            'type' : 'search_inprogress',
            "username": user
            }
            
        send_data = json.dumps(data)
        data = send_data.encode('utf-8')
        return data
    
    def unlock_car(self,car_id,booking_id): 
        """gnerate the unlock data for ap, when a use choose to unlock a car, it crete the unlock car_id data and the booking_id to the server """
        data={
            'car_id': car_id,
            'type' : 'unlock',
            "booking_id": booking_id
        }
         
        send_data = json.dumps(data)
        data = send_data.encode('utf-8')
        return data
    
    def return_car(self,car_id,booking_id):
        """gnerate the return data for ap, when a use choose to return a car, it crete the unlock car_id data and the booking_id to the server 
        also, it will generate the time and location information"""
        x,y= create_location()
        self.time=datetime.now()
        data ={
            "car_id": car_id,
            'type' : 'return_car',
            "booking_id": booking_id,
            "date_return": self.time.strftime('%Y-%m-%d'),
            "time_return": self.time.strftime('%H:%M:%S'),
            "status": "finished",
            "latitude": x,
            "longitude": y
        }
           
        send_data = json.dumps(data)
        data = send_data.encode('utf-8')
        return data