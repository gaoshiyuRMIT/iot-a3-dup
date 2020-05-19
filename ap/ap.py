from client import client as cl
from dataHelper import dataHelper as helper
import json
class ap():
    
    def __init__(self):
        self.username =None
        self.dataHelper = helper()
        self.cient = None
        
    def login(self,user, password):
        self.client = cl('127.0.0.1',61134)
        data = self.dataHelper.login(user, password)
        self.client.send_data(data)   
        status = self.client.listen_from_server() 
        if status == 'success':
            self.username=user
            print('you have sucessfully login')
            
        else:
            print ('wrong username or password.')    
            
        self.client.close_client()    
            
        # take in user input and use the cliend class to send client to a
    
    def find_booked_car(self): 
        #take in userid and return a list of car that is related to user, here pandas is recommended
        self.client = cl('127.0.0.1',61134)
        data = self.dataHelper.search_booking(self.username)
        self.client.send_data(data)
        bookings = self.client.listen_from_server() 
        self.load_all_cars(bookings)
        self.client.close_client()      
        
    def find_inprogress(self):
        self.client = cl('127.0.0.1',61134)
        data = self.dataHelper.search_inprogress(self.username)
        self.client.send_data(data)
        bookings = self.client.listen_from_server() 
        self.load_all_cars(bookings)
        self.client.close_client()
    
    def load_all_cars(self,data):
        bookings = json.loads(data)['data']
        num = 1
        if(len(bookings)!=0):   
            print("choose from the following car_ids: ")
            print("    car_id    booking_id")
            for book in bookings:
                print(("%d     %s          %s"  %(num,book['car_id'],book['booking_id'])))
                num+=1           
        else:
            print("you haven't booked any car")        
        
         
    
    def unlock_car(self, booking_id):
        self.client = cl('127.0.0.1',61134)
        data = self.dataHelper.unlock_car(booking_id)
        self.client.send_data(data)
        message = self.client.listen_from_server() 
        print(message)
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
    a1.login('xinhuanduan', 'a6096d7f16360d8ce5e81dfa947972f6')
    #a1.username = "yu"
    a1.find_booked_car()
    a1.find_inprogress()
    a1.unlock_car("5")
    # a1.return_car("1","1")