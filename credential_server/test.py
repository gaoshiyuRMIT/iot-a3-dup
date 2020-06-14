import unittest
from httpHelper import *
from dataHandler import *
import json
from datetime import datetime
helper = httpHelper()
handler = dataHandler ()

class serverTest(unittest.TestCase):
    def test_blue(self):
        response = handler.valid_bluetooth('70:EA:5A:33:54:52')
        self.assertNotEqual(response, 'fail')
        
    def test_neg_blue(self):
        response = handler.valid_bluetooth('70:EA:5A:33:54:51')
        self.assertEqual(response, 'fail')  
    
    def test_neg_QR(self):
        response = handler.valid_QR('xinhuan')
        self.assertEqual(response, 'fail')   
        
    def test_QR(self):
        response = handler.valid_QR('shiyu_engineer')
        self.assertNotEqual(response, 'fail')          
        
if __name__ == '__main__':
    unittest.main()  