import socket
import sys

from .httpHelper import httpHelper as Helper


# import a check credential function
class server:
    
    def __init__(self, port):
        self.s = socket.socket()
        self.s.bind(('',port))
        self.s.listen(5)  
        self.helper = Helper()  
        
    def handle_user(self,c):
        client_input = c.recv(1024).decode("utf-8") 
        result = self.helper.post(client_input)
        print(result)
        if result:
            self.send(c,"success")
        else:
            self.send(c,"fail")    
    
    def send(self,c,request):
       b = bytes(request,'utf-8')
       c.send(b) 
        
    def listen(self):
        while True:
            print('server is running')
            c,addr = self.s.accept()
            self.handle_user(c)
            print('accepted')
            self.handle_user    
            