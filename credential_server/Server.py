import socket
import sys
import json
from dataHandler import dataHandler as Handler
 
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
    s= server(61134)
    s.listen()
           
            