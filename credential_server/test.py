import unittest
from httpHelper import *
from dataHandler import *
import json
from datetime import datetime
helper = httpHelper()
handler = dataHandler ()

class serverTest(unittest.TestCase):
    def test_helper(self):
        response = handler.valid_bluetooth('70:EA:5A:33:54:52')
        self.assertEqual(response, 'success')
        
    def test_neg_helper(self):
        response = handler.valid_bluetooth('70:EA:5A:33:54:51')
        self.assertEqual(response, 'fail')  
        
        
if __name__ == '__main__':
    unittest.main()  