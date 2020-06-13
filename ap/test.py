import bluetooth
from dataHelper import dataHelper
from client import client

helper = dataHelper()
def send_and_valid(data):
    c = client()
    """
    sending and valid MAC address
    :param string data: the sent data
    :return: if the mac address is valid return true elase false
    :rtype: boolean
    """
    c.send_data(data)   
    status = c.listen_from_server() 
    c.close_client()
    if status == 'success':
        return True
        
def main():
    while(True):
        nearby_devices = bluetooth.discover_devices(lookup_names = True)
        print(len(nearby_devices))
        if len(nearby_devices)>0:
            print('welcome, {}'.format(nearby_devices[0][1]))
            bd_address=nearby_devices[0][0]
            print(bd_address)
            data = helper.validate_blue(bd_address)
            # if send_and_valid(data):
            #     exec(open("/home/pi/Desktop/IotA3/iot/ap/engineer.py").read())
            #     print('See u next time!')
            quit()
        else:
            print('no device found!')    

if __name__ == "__main__":
    
    main()