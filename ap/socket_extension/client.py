import socket    

class client:
    """
    This is a class used to connect to the server

    :param address: the ip address of the server
    :type address: string
    :param port: the port that the server is listening on
    :type port: int
    """
    def __init__(self, address, port):
        
        self.s = socket.socket()
        self.s.connect((address,port))
        

    
    def send_data(self, data):
        """send data to server
        
         :param string data: data to be sent to the server
        """
        self.s.send(data)
       
        
    def close_client(self):
        """close connection"""
        self.s.close()    
        
    def listen_from_server(self):
        """read data from server"""
        response = self.s.recv(1024).decode("utf-8")     
        return response    