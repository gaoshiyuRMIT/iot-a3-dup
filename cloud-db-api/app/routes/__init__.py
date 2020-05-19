from flask import url_for, request, Blueprint, g
from flask.json import jsonify
from app import app
from app.decorators import jsonifyResponseData

@app.route("/ping")
def ping():
    return "hello world"


from .bookings import bp as bookings_bp
from .cars import bp as cars_bp
from .users import bp as users_bp
