import os
from httpHelper import httpHelper as Helper
# from passlib.hash import sha256_crypt
import json
import pickle
# import jsonpickle
import pathlib
# import face_recognition
from pathlib import Path
import numpy as np

class dataHandler:
    CWD = os.getcwd()
    # ENCODEFOLDER = "../admin-app/app/dataset/{}/encoding"
    # ENCODEFILEPATH = CWD + "/iot/admin-app/app/dataset/{}/encoding/face_encoding.pickle"
    ENCODEFOLDER = os.path.realpath("../admin-app/app/dataset/{}/encoding")

    def __init__(self):
        self.helper = Helper()
    
    def hanle_data(self,data):
        """choose diffrent function according to the data type
        :param dict: a dictionary recieved from the client 
        """
        if data['type'] == 'login':
            return self.login(data)
        # elif data['type'] == 'loginface':
        #     return self.login_face(data)
        elif data['type'] == 'search_booking':
            return self.search_booking(data,"booked")
        elif data['type'] == 'search_inprogress':
            return self.search_booking(data,"inProgress")
        elif data['type'] == 'unlock':
            return self.unlock(data)
        elif data['type'] == 'valid_QR':
            return self.valid_QR(data['decode'])
        elif data['type'] == 'valid_blue':
            return self.valid_bluetooth(data['MAC'])
        else:
            return self.return_car(data)
        
    def return_car(self, data):
        """change database via api, return situation
        :param string: a dictionary recieved from the client 
        :return: the data that will be sent via socket
        :rtype: string
         """
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
        """change  database via api, unlock situation
        :param string: a dictionary recieved from the client 
        :return: the data that will be sent via socket
        :rtype: string
         """
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
        """get data from database, search situation 
        :param string: a dictionary recieved from the client 
        :return: the data that will be sent via socket
        :rtype: string
        """
        data = {
           "username" : user_input['username'],
           "status" : status
        }
        response = self.helper.post_data('/bookings/search',data) 
        return response.text
        
    # def login(self, user_input):
    #     """the login function, communicate with the database and valid credential
    #     :param string: a dictionary recieved from the client 
    #     :return: the data that will be sent via socket
    #     :rtype: string
    #     """
    #     data = {
    #        "username" :  user_input['username']
    #     }
    #     response = self.helper.post_data('/users/search', data)
    #     login_details = json.loads(response.text) 
    #     if login_details['data']['success']:
    #         passwordhash = login_details['data']['user']['password']
    #         print(passwordhash)
    #         password = user_input['password']
    #         print(password)
    #         print(sha256_crypt.verify(password, passwordhash))
    #         if sha256_crypt.verify(password, passwordhash):
    #             return "success"
        
    #     return 'fail'

    def get_encode_file_path(self, username):
        return os.path.realpath(f"../admin-app/datasets/{username}/encoding/face_encoding.pickle")

    
    # def login_face(self, data):
    #     """login face compares the encoding of the supplied image to the
    #     encodings on file for the user to ascertain whether the user is 
    #     who they say they are.
    #     login face compares the encoding of the supplied image to the
    #     encodings on file for the user to ascertain whether the user is 
    #     who they say they are.
    #     :param string data: a dictionary recieved from the client 
    #     :return: the data that will be sent via socket
    #     :rtype: string
    #     """
    #     data_dict = data
    #     #(dict containing keys: "type" (loginface) "username" and "encodings"(pickled encodings 
    #     # of numpy darray)
    #     submitted_encoding = data_dict["encodings"]
    #     submitted_encoding = [np.array(l) for l in submitted_encoding][0]
	# 	#'encodings' can now be compared to what the master pi has on file to confirm user identity
    #     # get stored encodings:
    #     name = data_dict["username"] 
    #     #get predicted file path to encoding of user
    #     # user_encodings = self.get_encode_file_path(name)
    #     # check file exists:
    #     user_encodings_file = self.get_encode_file_path(name)
    #     if os.path.isfile(user_encodings_file):
    #         user_encodings = None
    #         with open(user_encodings_file, "rb") as fh:
    #             stored_dict = pickle.load(fh)
    #             user_encodings = stored_dict["encodings"]
    #             user_encodings = [l[0] for l in user_encodings]
    #         #compare submitted image to stored images
    #         matches = face_recognition.compare_faces(user_encodings, submitted_encoding, tolerance=0.8) # outputs list of arrays size 128 - one per comparison - each value being true or false 
    #         pos = 0
    #         for match in matches:
    #             if match:
    #                 pos += 1
    #         return "success" if float(pos) / len(matches) >= 0.8 else "failed"
    #     #else file does not exist (either user doesnt exist or they havent done face recognition process)
    #     else:
    #         return "failed"
    
    def update_car(self, car, car_id):
        """update car data
        :param string car: car is a json string
        :return: the data that will be sent via socket
        :rtype: string
        """
        response = self.helper.put(('/cars/%s/update' %car_id), car)   
    
    def update_booking(self,booking_id,booking):
        """update booking data
        :param string booking_id: the booking id of the booking
        :param string booking: the booking data to be put in the database
        """
        response = self.helper.put(('/bookings/%s/update' %booking_id),booking)
        
    def valid_bluetooth(self, MAC):
        """update booking data
        :param string MAC: the MAC address recieved from the user
        :return: the data that will be sent via socket(either fail or the user)
        :rtype: string
        """
        response = self.helper.get('/employees/engineers/mac/%s' %MAC)
        if(response.status_code == 200):
            return response.text
        else:
            return 'fail'
        
    def valid_QR(self, username):
        """update booking data
        :param string username: the user name of the engineer
        :return: the data that will be sent via socket(either fail or the user)
        :rtype: string
        """  
        response = self.helper.get('/employees/engineers/%s' %username)
        if(response.status_code == 200):
            return response.text
        else:
            return 'fail'
    
    