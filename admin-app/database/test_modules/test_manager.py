from iot.test_modules.test_booking_manager import TestBookingManager
from iot.test_modules.test_user_manager import TestUserManager
from iot.test_modules.test_car_manager import TestCarManager
import unittest
import logging
import sys


def suite(self):
    # create a test suite which has all test methods from each DB manager test class
    suite = unittest.TestSuite()
    suite = suite.unittest.TestLoader().loadTestsFromTestCase(TestCarManager)
    suite += suite.unittest.TestLoader().loadTestsFromTestCase(TestUserManager)
    suite += unittest.TestLoader().loadTestsFromTestCase(TestBookingManager)
    return suite


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
