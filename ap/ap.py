from .client import client as cl
from .dataHelper import dataHelper as helper
class ap():
    
    def __init__(self):
        self.username =None
        self.dataHelper = helper()
        self.cient = None
        
    def login(self,user, password):
        self.client = cl('127.0.0.1',61134)
        response = self.client.send_credential(user,password)
        if response== "success":
            self.username = user
            print('sucess')
        else:
            print('wrong password or wrong user name')
            
        # take in user input and use the cliend class to send client to a
    def find_brelated_car(self,userId):
        #take in userid and return a list of car that is related to user, here pandas is recommended
        return
    
    def get_return_list(self):
        #use panda to generate a list of car that is returnnable from the userdatetime A combination of a date and a time. 
        return
    
    def get_past_list(self):
            #use panda to generate a list of car that has been returned by the user from the userdatetime A combination of a date and a time. 
        return
    
    def show_available_car(self):
        # still using panda
        return
    
    def unlock_car(self, car_id):
        data = self.dataHelper.unlock(car_id,self.username)
        self.client.send_data(data)
        return
    
    def return_car(self,car_id):
        return