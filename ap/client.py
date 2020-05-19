import socket    

class client:
    def __init__(self, address, port):
        self.s = socket.socket()
        self.s.connect((address,port))
        print('client set up')
        

    
    def send_data(self, data):
        self.s.send(data)
        #response = self.listen_from_server();
        #return response
        
    def close_client(self):
        self.s.close()    
        
    def listen_from_server(self):
        response = self.s.recv(1024).decode("utf-8")     
        return response    