from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from . import routes
from .BookingManager import BookingManager
from .CarManager import CarManager