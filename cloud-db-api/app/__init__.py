from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from .routes import bookings_bp, cars_bp, users_bp

app.register_blueprint(bookings_bp)
app.register_blueprint(cars_bp)
app.register_blueprint(users_bp)

from .BookingManager import BookingManager
from .CarManager import CarManager
from .UserManager import UserManager
from .errors import handlers
