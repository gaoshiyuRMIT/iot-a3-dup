from datetime import datetime
import json
class dataHelper:
    def __init__(self):
        self.time = None
        
    def login(self, username, password):
        data={
            'type' : 'login',
            "username": username, 
            "password": password
        }
          
        send_data = json.dumps(data)
        data = send_data.encode('utf-8')
        return data
    
        
    def search_booking(self,user):
        self.time=datetime.now()
        data={
            'type' : 'search_booking',
            "username": user
            }
            
        send_data = json.dumps(data)
        data = send_data.encode('utf-8')
        return data
    
    def search_inprogress(self,user):
        self.time=datetime.now()
        data={
            'type' : 'search_inprogress',
            "username": user
            }
            
        send_data = json.dumps(data)
        data = send_data.encode('utf-8')
        return data
    
    def unlock_car(self,booking_id): 
        data={
            'type' : 'unlock',
            "booking_id": booking_id
        }
         
        send_data = json.dumps(data)
        data = send_data.encode('utf-8')
        return data
    
    def return_car(self,car_id,booking_id):
        self.time=datetime.now()
        data ={
            'type' : 'return_car',
            "status": "available",
            "booking_id": booking_id,
            "date_return": self.time.strftime('%Y-%m-%d'),
            "time_return": self.time.strftime('%H:%M:%S'),
            "status": "finished"
        }
           
        send_data = json.dumps(data)
        data = send_data.encode('utf-8')
        return data