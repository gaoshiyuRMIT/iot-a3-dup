import bluetooth
from dataHelper import dataHelper
from client import client
from configparser import ConfigParser

class console:
    helper = dataHelper()
    config = ConfigParser()
    config.read('ap.config', encoding='UTF-8')
    port=config['address'].getint('port')
    ip = config['address'].get('ip')
    username = None
    def send_and_valid(self,data):
        """
        sending and valid MAC address
        :param string data: the sent data
        :return: if the mac address is valid return true elase false
        :rtype: boolean
        """
        c = client(self.ip,self.port)
        c.send_data(data)   
        status = c.listen_from_server() 
        c.close_client()
        if status == 'fail':
            return False
        else:
            username = status['data']['fName']
            return True
        
    def main(self):
        while(True):
            nearby_devices = bluetooth.discover_devices(duration =8,lookup_names = True)
            
            if len(nearby_devices)>0:
                for address, name in nearby_devices:
                    print(address)
                    data = self.helper.validate_blue(bd_address)
                    if send_and_valid(data):
                        print('welcome, {}!'.format(username))
                        exec(open("/home/pi/Desktop/IotA3/iot/ap/engineer.py").read())
                        print('See u next time!')
                    quit()
            else:
                print('no device found!')    

if __name__ == "__main__":
    
    main()