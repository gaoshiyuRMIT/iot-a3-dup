import bluetooth
from dataHelper import dataHelper

helper = dataHelper()
helper.

while(True):
    nearby_devices = bluetooth.discover_devices(lookup_names = True)
    print(len(nearby_devices))
    if len(nearby_devices)>0:
        print('welcome, {}'.format(nearby_devices[0][1]))
        bd_address=nearby_devices[0][0]
        print(len(nearby_devices))
        exec(open("/home/pi/Desktop/IotA3/iot/ap/engineer.py").read())
        print('See u next time!')
        quit()
    else:
        print('no device found!')    

