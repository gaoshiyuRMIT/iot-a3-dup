from client import client as cl
from dataHelper import dataHelper as helper
import json
import hashlib
from configparser import ConfigParser

config = ConfigParser()
config.read('ap.config', encoding='UTF-8')
port=config['address'].getint('port')
ip = config['address'].get('ip')

class ap():
    
    def __init__(self):
        self.username =None
        self.dataHelper = helper()
        self.cient = None
        
    def login(self,user, password):
        islogin = False
        self.client = cl(ip,port)
        data = self.dataHelper.login(user, password)
        self.client.send_data(data)   
        status = self.client.listen_from_server() 
        if status == 'success':
            self.username=user
            print('you have sucessfully login')
            islogin=True           
        else:
            print ('wrong username or password.')          
        self.client.close_client()   
        return islogin 
            
        # take in user input and use the cliend class to send client to a
    
    def find_booked_car(self): 
        #take in userid and return a list of car that is related to user, here pandas is recommended
        self.client = cl(ip,port)
        data = self.dataHelper.search_booking(self.username)
        self.client.send_data(data)
        bookings = self.client.listen_from_server() 
        bookings = json.loads(bookings)['data']
        choice = self.load_all_cars(bookings,'booked')
        self.client.close_client()
        if(choice!=None):      
            self.unlock_car(bookings[choice]["booking_id"])
        
    def find_inprogress(self):
        self.client = cl(ip,port)
        data = self.dataHelper.search_inprogress(self.username)
        self.client.send_data(data)
        bookings = self.client.listen_from_server() 
        bookings = json.loads(bookings)['data']
        choice =self.load_all_cars(bookings,'unlocked')
        self.client.close_client()
        if(choice!=None):
            self.return_car(bookings[choice]['car_id'],bookings[choice]["booking_id"])
    
    def load_all_cars(self,bookings,type):
        num = 1
        if(len(bookings)!=0):   
            print("choose from the following car_ids: ")
            print("    car_id    booking_id")
            for book in bookings:
                print(("%d     %s          %s"  %(num,book['car_id'],book['booking_id'])))
                num+=1       
            choice = input()
            return int(choice)-1
        else:
            print(("you haven't %s any car" %type))        
            return None
         
    
    def unlock_car(self, booking_id):
        self.client = cl(ip,port)
        data = self.dataHelper.unlock_car(booking_id)
        self.client.send_data(data)
        message = self.client.listen_from_server() 
        print(message)
        self.client.close_client() 
        
    
    def return_car(self,car_id,booking_id):
        self.client = cl(ip,port)
        data = self.dataHelper.return_car(car_id,booking_id)
        self.client.send_data(data)
        message = self.client.listen_from_server() 
        print(message)
        self.client.close_client() 
        
    
    def input_credential(self):
        print("input your user name")
        username = input()
        print("input your password")
        password = input()
        h = hashlib.md5(password.encode())
        password=h.hexdigest()
        return username,password
        
if __name__ == "__main__":
    a1= ap()
    # a1.login('xinhuanduan', 'a6096d7f16360d8ce5e81dfa947972f6')
    #a1.username = "yu"
    # a1.find_booked_car()
    a1.find_inprogress()
    # a1.unlock_car("5")
    a1.return_car(1,"5")