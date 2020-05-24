from httpHelper import httpHelper as Helper
from passlib.hash import sha256_crypt
import json
import pickle
import jsonpickle
import face_recognition
from pathlib import Path
import numpy as np

class dataHandler:
    CWD = str(pathlib.Path.cwd())
    ENCODEFOLDER = "./iot/admin-app/app/dataset/{}/encoding"
    ENCODEFILEPATH = CWD + "/iot/admin-app/app/dataset/{}/encoding/face_encoding.pickle"

    def __init__(self):
        self.helper = Helper()
    
    def hanle_data(self,data):
        """choose diffrent function according to the data type"""
        if data['type'] == 'login':
            return self.login(data)
        elif data['type'] == 'loginface':
            return self.login_face(data)
        elif data['type'] == 'search_booking':
            return self.search_booking(data,"booked")
        elif data['type'] == 'search_inprogress':
            return self.search_booking(data,"inProgress")
        elif data['type'] == 'unlock':
            return self.unlock(data)
        else:
            return self.return_car(data)
        
    def return_car(self, data):
        """change database via api, return situation """
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
        """change  database via api, unlock situation """
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
        """get data from database, search situation """
        data = {
           "username" : user_input['username'],
           "status" : status
        }
        response = self.helper.post_data('/bookings/search',data) 
        return response.text
        
    def login(self, user_input):
        """the login function, communicate with the database and valid credential """
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

    """login face compares the encoding of the supplied image to the
    encodings on file for the user to ascertain whether the user is 
    who they say they are."""
    def login_face(self, data):
        # decode from bytes to jsonpickle string
        rec_data = data.decode('utf-8')
		#decode from jsonpickle
        data_dict = jsonpickle.decode(rec_data)
        #(dict containing keys: "type" (loginface) "username" and "encodings"(pickled encodings 
        # of numpy darray)
        submitted_encoding = pickle.loads(data_dict["encodings"])
		#'encodings' can now be compared to what the master pi has on file to confirm user identity
        # get stored encodings:
        name = data_dict["username"] 
        #get predicted file path to encoding of user
        user_encodings = Path(ENCODEFILEPATH.format(name))
        # check file exists:
        if user_encodings.is_file():
        # file exists
            #compare submitted image to stored images
            matches = face_recognition.compare_faces(user_encodings, submitted_encoding, tolerance=0.1) # outputs list of arrays size 128 - one per comparison - each value being true or false 
            neg, pos = 0
            for count, item in enumerate(matches): #count is seperate arrays (of size 128), item are the actual arrays
                #coutn True results in each array and deduce False results
                sum_pos = np.sum(item)
                neg += (128 - sum_pos)
                #average false results, more then 10 False results per image == not a match
                average_result = neg/(count + 1)
                if average_result > 10:
                    return "failed"
                else:
                    return "success"
        #else file does not exist (either user doesnt exist or they havent done face recognition process)
        else:
            return "failed"
    
    def update_car(self, car, car_id):
        """update car data"""
        response = self.helper.put(('/cars/%s/update' %car_id), car)   
    
    def update_booking(self,booking_id,booking):
        """update booking data"""
        response = self.helper.put(('/bookings/%s/update' %booking_id),booking)
        
    
    
    
    