from httpHelper import httpHelper as Helper
import json

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
            return self.unlock(data['booking_id'])
        else:
            update_car(data['id'])
            update_booking(data['id'])
            
        
        
    def unlock(self,booking_id):
        booking={
            'status' : 'inProgress'
        }  
        self.update_booking(booking_id,booking) 
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
           "username" :  user_input['username'],
           "password" : user_input["password"]
        }
        response = self.helper.post_data('/users/login', data)
        login_details = json.loads(response.text) 
        if login_details['data']['success']:
            return "success"
        else:
            return 'fail'
    
    def update_car(self, car, car_id):
        response = self.helper.put(('/cars/%s/update' %car_id), car)   
    
    def update_booking(self,booking_id,booking):
        response = self.helper.put(('/bookings/%s/update' %booking_id),booking)
        
    
    
    
    def return_car(self,booking_id, car_id, data):
        booking={
            'status' :'finished',
        }
        self.update_booking()    