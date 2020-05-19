import socket
import sys
import json
from httpHelper import httpHelper as Helper
 
# import a check credential function
class server:
    
    def __init__(self, port):
        self.s = socket.socket()
        self.s.bind(('',port))
        self.s.listen(5)  
        self.helper = Helper()  
        self.c = None
    
    def send(self,c,request):
       b = bytes(request,'utf-8')
       c.send(b) 
       
    def read_data(self):
        client_input = self.c.recv(1024)
        #data = json.loads(client_input)
        print(client_input)
           
        
    def listen(self):
        print('server is running')
        while True:
            
            try:
                c,addr = self.s.accept()
                self.c=c
                self.read_data()
            except:
                print('client fault')
            
if __name__ == "__main__":
    s= server(61134)
    s.listen()
           
            