from httpHelper import httpHelper as Helper
import json
from passlib.hash import sha256_crypt

class dataHandler:
    def __init__(self):
        self.helper = Helper()
    
    def hanle_data(self,data):
        if data['type'] == 'login':
            return self.login(data)
        
        elif data['type'] == 'search_booking':
            return self.search_booking(data,"booked")
        elif data['type'] == 'search_inprogress':
            return self.search_booking(data,"inprogress")
        elif data['type'] == 'unlock':
            return self.unlock(data)
        else:
            return self.return_car(data)
        
    def return_car(self, data):
        booking={
        'status' :'finished',
        "date_return": data['date_return'],  
        "time_return": data['time_return'],
       
    }
        self.update_booking(data['booking_id'],booking)     
        
        car={
            'car_status': 'available',
            "latitude": data['latitude'],
            "longitude":data['longitude']
        }  
        
        self.update_car(car,data['car_id'])
        return "you have successfully returned the car" 
        
    def unlock(self,data):
        booking={
            'status' : 'inProgress'
        }  
        self.update_booking(data['booking_id'],booking) 
        car={
            'car_status': 'inUse'
        }  
        
        self.update_car(car,data['car_id'])
        return "you have successfully unlocked the car" 
    
    def search_booking(self,user_input,status):
        data = {
           "username" : user_input['username'],
           "status" : status
        }
        response = self.helper.post_data('/bookings/search',data) 
        return response.text
        
    def login(self, user_input):
        data = {
           "username" :  user_input['username']
        }
        response = self.helper.post_data('/users/search', data)
        login_details = json.loads(response.text) 
        if login_details['data']['success']:
            passwordhash = login_details['data']['user']['password']
            print(passwordhash)
            password = user_input['password']
            print(password)
            print(sha256_crypt.verify(password, passwordhash))
            if sha256_crypt.verify(password, passwordhash):
                return "success"
        
        return 'fail'
    
    def update_car(self, car, car_id):
        response = self.helper.put(('/cars/%s/update' %car_id), car)   
    
    def update_booking(self,booking_id,booking):
        response = self.helper.put(('/bookings/%s/update' %booking_id),booking)
        
    
    
    
    