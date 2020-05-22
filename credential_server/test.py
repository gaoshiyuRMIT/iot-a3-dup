import unittest
from httpHelper import *
import json
from datetime import datetime
helper = httpHelper()

class serverTest(unittest.TestCase):
    def test_get(self):
        
        response = helper.get("/cars/search?status=available")
        self.assertEqual((json.loads(response.text)['data'][0]['status']), 'available')
        
    def test_post(self): 
        now = datetime.now()   
        data ={
            "car_id": 1,
            "date_booking": now.strftime('%Y-%m-%d'),
            "time_booking": now.strftime('%H-%M-%S'),
            "username": "janedoe1"
        }
        response = helper.post_data('/bookings/add',data)
        self.assertEqual((json.loads(response.text)['data']['booking_id']), 1)
        self.assertEqual(now.strftime('%Y-%m-%d'), '2020-05-09')
        
    def test_put(self):
        data={
            "date_return": "2020-06-05",
            "time_return": "11:00:00"
        }
        response = helper.put('/bookings/1/update',data)
        self.assertEqual((json.loads(response.text)['data']['success']), True)
        
if __name__ == '__main__':
    unittest.main()  