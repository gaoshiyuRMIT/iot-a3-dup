from flask import Blueprint, request
from app.services.car_service import CarService
from app.services.user_service import UserService

bp = Blueprint("dashboard", __name__, "/dashboard")

@bp.route("/")
def dashboard():
    pass

