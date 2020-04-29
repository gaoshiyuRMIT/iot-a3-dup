from flask import url_for, request
from flask.json import jsonify
from app import app
from app.CarManager import CarManager
from app.BookingManager import BookingManager
from app.UserManager import UserManager

carMgr = CarManager()
bkMgr = BookingManager()
usMgr = UserManager()

from .bookings import bookings, updateBooking, addBooking
from .cars import cars, updateCar, addCar
from .users import register, login
