import socket    

class client:
    def __init__(self, address, port):
        self.s = socket.socket()
        self.s.connect((address,port))
        print('client set up')
    def send_credential(self, user_name, password):
        credential = (user_name + '/%s' %password)
        b=bytes(credential, 'utf-8')
        self.s.send(b)    
        response = self.listen_from_server()
        print(response)
    def close_client(self):
        self.s.close()    
        
    def listen_from_server(self):
        response = self.s.recv(1024).decode("utf-8")     
        return response    