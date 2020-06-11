import matplotlib
matplotlib.use('Agg')
from tkinter import Tk, filedialog
import os
from pyzbar import pyzbar
import cv2
class QR_reader:
    def get_path(self):
        """
        call a window to let user choose photoes
        :return string: the file path chosen by the user
        """
        Tk().withdraw()        
        image_filepath = filedialog.askopenfilename(filetypes=[("jpg files", "*.jpg")], initialdir='/home/pi/Desktop/IotA3/iot/ap/QRCode/Images', title="Choose a QR code image")
        return image_filepath

    def scan_QR(self):
        """
        scan the QR code
        :param string: the encode data
        :return string: the Json String decoded from the QR code
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
            barcodeType = barcode.type
            # print the barcode type and data to the terminal
            print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
      
