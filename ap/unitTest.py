import unittest
from agent import *
import json
from datetime import datetime


class serverTest(unittest.TestCase):
    
    def test_login_positive(self):
        a = ap()
        islogin = a.login("shiyu_admin","Abcd1234")
        self.assertTrue(islogin)
        
    def test_login_negative(self): 
        a = ap()
        islogin = a.login("shiyu_admin","abcd1234")
        self.assertFalse(islogin)
        
    def test_load_booked(self):
        a = ap()
        a.username = "shiyu_admin"
        bookings = a.load_booking("booked")
        self.assertEqual(bookings, [])
        
    # def test_load_booked(self):
    #     a = ap()
    #     a.username = "shiyu_admin"
    #     bookings = a.load_booking("inProgress")
    #     self.assertEqual(bookings, [])  
        
if __name__ == '__main__':
    unittest.main()  