import socket
import sys
import json
from dataHandler import dataHandler as Handler
from configparser import ConfigParser

 
# import a check credential function
class server:
    
    def __init__(self, port):
        self.s = socket.socket()
        self.s.bind(('',port))
        self.s.listen(5)       
        self.c = None
        self.handle =Handler()
    
    def send(self,request):
       b = bytes(request,'utf-8')
       print('sending...' + request)
       self.c.send(b) 
       
    def read_data(self):
        client_input = self.c.recv(1024)
        data = json.loads(client_input)
        self.send(self.handle.hanle_data(data))
           
        
    def listen(self):
        print('server is running')
        while True:

                c,addr = self.s.accept()
                self.c=c
                self.read_data()
         
               
            
if __name__ == "__main__":
    config = ConfigParser()
    config.read('ap.config', encoding='UTF-8')
    port=config['address'].getint('port')
    s= server(port)
    s.listen()
           
            
# in another vs code window, the server is running, as you can see in the lest, I only open the credential_server folder
# can u see me typing? talk to me I can hear you
#so I will run the server now...
#server is running
#now i will swap to the ap side
# can I?
