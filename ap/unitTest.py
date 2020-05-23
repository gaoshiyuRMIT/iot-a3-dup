import unittest
from agent import *
import json
from datetime import datetime


class serverTest(unittest.TestCase):
    
    def test_load_booked(self):
        a = ap()
        a.username = "shiyu_admin"
        bookings = a.load_booking("booked")
        self.assertEqual(bookings, [])
        
    def test_load_inProgress(self):
        a = ap()
        a.username = "shiyu_admin"
        bookings = a.load_booking("inProgress")
        self.assertEqual(bookings, [])  
    
    def test_login_positive(self):
        a = ap()
        islogin = a.login("shiyu_admin","Abcd1234")
        self.assertTrue(islogin)
        
    def test_login_negative(self): 
        a = ap()
        islogin = a.login("shiyu_admin","abcd1234")
        self.assertFalse(islogin)
        
    def test_login_unlock(self): 
        a = ap()
        a.username = "shiyu_admin"
        message = a.upload(1,1,"unlock")
        self.assertEqual(message, 'you have successfully unlocked the car')  
          
        
    def test_login_ureturn(self): 
        a = ap()
        a.username = "shiyu_admin"
        message = a.upload(1,1,"return")
        self.assertEqual(message, 'you have successfully returned the car')   
        
    
        
if __name__ == '__main__':
    unittest.main()  