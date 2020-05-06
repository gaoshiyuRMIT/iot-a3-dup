import socket
import sys

# import a check credential function
class server:
    
    def __init__(self, port):
        self.s = socket.socket()
        self.s.bind(('',port))
        self.s.listen(5)    
    def listen(self):
        while True:
            print('server is running')
            c,addr = self.s.accept()
            print('accept')
            jkl = c.recv(1024).decode("utf-8")    
            print(jkl)