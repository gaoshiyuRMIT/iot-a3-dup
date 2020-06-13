import socket    

class client:
    def __init__(self, address, port):
        self.s = socket.socket()
        self.s.connect((address,port))
        

    
    def send_data(self, data):
        """send data to server
         :param string data: data to be sent to the server
        """
        self.s.send(data)
        #response = self.listen_from_server();
        #return response
        
    def close_client(self):
        """close connection"""
        self.s.close()    
        
    def listen_from_server(self):
        """read data from server"""
        response = self.s.recv(1024).decode("utf-8")     
        return response    