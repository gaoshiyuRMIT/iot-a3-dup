from httpHelper import httpHelper as Helper

class dataHandler:
    def __init__(self):
        self.helper = Helper
    
    def hanle_data(self,data):
        globals()[data[0]['type']](self, data)
            
        
        
    def login(self, data):
        response = self.helper.post_data('/users/login', data[1]) 
    
    def update_car(self, car, car_id):
        response = self.helper.put(('/cars/%s/update' %car_id), car)   
    
    def update_booking(self,booking_id,booking):
        response = self.helper.put(('/bookings/%s/update' %booking_id),booking)
        
    def unlock(self,booking_id):
        booking={
            'status' : 'inProgress'
        }  
        self.update_booking(booking_id,booking)
    
    def search_booking(self,data):
        response = self.helper.put('/bookings/search',data[1])
    
    def return_car(self,booking_id, car_id, data):
        booking={
            'status' :'finished',
        }
        self.update_booking()    