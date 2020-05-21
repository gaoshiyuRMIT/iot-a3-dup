from client import client as cl
from dataHelper import dataHelper as helper
from captureface import CaptureFace
import json
import hashlib

class ap():
    
    def __init__(self):
        self.username = None
        self.dataHelper = helper()
        self.cient = None
        
    def login(self, user, password):
        islogin = False
        self.client = cl('127.0.0.1', 61134)
        data = self.dataHelper.login(user, password)
        self.client.send_data(data)   
        status = self.client.listen_from_server() 
        if status == 'success':
            self.username = user
            print('you have sucessfully login')
            islogin = True           
        else:
            print ('wrong username or password.')          
        self.client.close_client()   
        return islogin
        # take in user input and use the client class to send client to a

    def login_face(self, p_data):
        islogin = False
        self.client = cl('127.0.0.1', 61134)
        data = self.dataHelper.login_face(p_data)
        self.client.send_data(data)
        status = self.client.listen_from_server()
        if status == 'success':
            print('you have sucessfully logged in')
            islogin = True
        else:
            print('your face was not recognised!')
        self.client.close_client()
        return islogin


    def find_booked_car(self):
        #take in userid and return a list of car that is related to user, here pandas is recommended
        self.client = cl('127.0.0.1',61134)
        data = self.dataHelper.search_booking(self.username)
        self.client.send_data(data)
        bookings = self.client.listen_from_server() 
        bookings = json.loads(bookings)['data']
        choice = self.load_all_cars(bookings,'booked')
        self.client.close_client()
        if(choice!=None):      
            self.unlock_car(bookings[choice]["booking_id"])
        
    def find_inprogress(self):
        self.client = cl('127.0.0.1',61134)
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
        self.client = cl('127.0.0.1',61134)
        data = self.dataHelper.unlock_car(booking_id)
        self.client.send_data(data)
        message = self.client.listen_from_server() 
        print(message)
        self.client.close_client() 
        
    
    def return_car(self,car_id,booking_id):
        self.client = cl('127.0.0.1',61134)
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

    """input_image_credentials coordinates the capturing of a facial image
    either via PiCam or uploaded file. and returns pickled encoding
    for comparison with encodings on Master Pi."""
    def input_image_credential(self):
        capture = CaptureFace()
        input_valid = False
        while input_valid is not True:
            print("\n\nFacial recognition requires a photo of your face: ")
            choice = input("""Enter '1' to take a photo using PiCam \nEnter '2' to choose a photo from file \n""")
            if choice == '1' or choice == '2':
                input_valid = True
            else:
                print("You must enter '1' or '2'. Please try again.")
        if choice == '1':
            capture.retrieve_webcam_image()
            p_data = capture.encode_image()
            return p_data
        else:
            capture.retrieve_image_from_file()
            p_data = capture.encode_image()
            return p_data

if __name__ == "__main__":
    a1= ap()
    # a1.login('xinhuanduan', 'a6096d7f16360d8ce5e81dfa947972f6')
    #a1.username = "yu"
    # a1.find_booked_car()
    a1.find_inprogress()
    # a1.unlock_car("5")
    a1.return_car(1,"5")