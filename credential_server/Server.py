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
        """ SEND DATA TO THE CLIENT """
        b = bytes(request,'utf-8')
        print('sending...' + request)
        self.c.send(b) 
       
    def read_data(self):
        """ read DATA from THE CLIENT """
        client_input = self.c.recv(1024)
        data = json.loads(client_input)
        self.send(self.handle.hanle_data(data))
           
        
    def listen(self):
        """the run function for client"""
        print('server is running')
        while True:
            c,addr = self.s.accept()
            self.c=c
            self.read_data()

    def stop(self):
        self.s.shutdown()
        self.s.close()
         
               
            
if __name__ == "__main__":
    config = ConfigParser()
    config.read('ap.config', encoding='UTF-8')
    port=config['address'].getint('port')
    s= server(port)
    try:
        s.listen()
    except KeyboardInterrupt:
        s.stop()