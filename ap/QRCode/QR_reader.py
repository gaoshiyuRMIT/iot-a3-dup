from pyzbar import pyzbar
import cv2
from dataHelper import dataHelper
from client import client
import json
from configparser import ConfigParser
from tabulate import tabulate
helper = dataHelper()


class QR_reader:
    def __init__(self):
        config = ConfigParser()
        config.read('ap.config', encoding='UTF-8')
        self.port=config['address'].getint('port')
        self.ip = config['address'].get('ip')
    def get_path(self):
        """
        call a window to let user choose photoes
        :return: the file path chosen by the user
        :rtype: string
        """
        print("input a file path of your qrcode")     
        image_filepath = input()
        return image_filepath

    def scan_QR(self):
        """
        scan the QR code
        :param string: the encode data
        :return: the Json String decoded from the QR code
        :rtype: string
        """   
        path = self.get_path()
        image = cv2.imread(path)
        barcodes = pyzbar.decode(image)
        print(len(barcodes))
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw the
            # bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # the barcode data is a bytes object so if we want to draw it on
            # our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            username = json.loads(barcodeData)['name']
            self.send_and_recieve(username)   

    def send_and_recieve(self,data):
        """
        sending and valid username decoded from the QR code
        :param string data: user name

        """
        c=client(self.ip, self.port)
        valid_data =helper.valid_QR(data)
        c.send_data(valid_data)   
        engineereer_data = c.listen_from_server() 
        c.close_client()
        if(engineereer_data=='fail'):
            print('unstable QR code')
        else:    
            profile_data = json.loads(engineereer_data)
            print('engineer info:')
            tp = self.get_tabulate(profile_data['data'])
            print(tp)   

    def get_tabulate(self, user):
        """
        return a tabulate table
        :param string user: a json or dict of the user
        :return: a tabulate tableof user
        :rtype: tabulate
        """
        tb = tabulate([['name', user['fName']],['experience',user['experience']],['email',user['email']]],headers=['key','value'],tablefmt='orgtbl')
        return tb
if __name__ == "__main__":
    
    reader = QR_reader()
    reader.scan_QR()