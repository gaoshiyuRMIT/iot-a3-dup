from client import client as cl
from dataHelper import dataHelper as helper
class ap():
    
    def __init__(self):
        self.username =None
        self.dataHelper = helper()
        self.cient = None
        
    def login(self,user, password):
        self.client = cl('127.0.0.1',61134)
        data = self.dataHelper.login(user, password)
        self.client.send_data(data)
        self.client.close_client()    
        self.username=user
            
        # take in user input and use the cliend class to send client to a
    def find_booked_car(self): 
        #take in userid and return a list of car that is related to user, here pandas is recommended
        self.client = cl('127.0.0.1',61134)
        data = self.dataHelper.search_booking(self.username,status = 'available')
        self.client.send_data(data)
        self.client.close_client()    
    
    
    def unlock_car(self, booking_id):
        self.client = cl('127.0.0.1',61134)
        data = self.dataHelper.unlock_car(booking_id)
        self.client.send_data(data)
        self.client.close_client() 
        return
    
    def return_car(self,car_id,booking_id):
        self.client = cl('127.0.0.1',61134)
        data = self.dataHelper.return_car(car_id,booking_id)
        self.client.send_data(data)
        self.client.close_client() 
        return
    
    def input_credential(self):
        print("input your user name")
        username = input()
        print("input your password")
        password = input()
        return username,password
        
if __name__ == "__main__":
    a1= ap()
    a1.login('1234568', 'xinhuan')
    a1.find_booked_car()
    a1.unlock_car("1")
    a1.return_car("1","1")