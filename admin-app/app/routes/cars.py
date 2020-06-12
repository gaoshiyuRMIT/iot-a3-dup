from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from app.services.car_service import CarService
from app.services.booking_service import BookingService
from app.services.admintalk import AdminTalk


bp = Blueprint("cars", __name__, url_prefix="/cars")

@bp.route("/<int:car_id>/map")
def show_car_on_map(car_id):
    pass

@bp.route("/reported")
def list_cars_reported_with_issues():
    pass


@bp.route("/add")
def add_car_page():
    pass

@bp.route("/add", methods=["POST"])
def add_car():
    # get new car info from request.form
    pass

@bp.route("/<int:car_id>/bookings")
def rental_history(car_id):
    pass

@bp.route("/<int:car_id>/update")
def update_car_page(car_id):
    pass

@bp.route("/<int:car_id>/update", methods=["PUT"])
def update_car(car_id):
    # get new car info from request.form
    pass

@bp.route("/<int:car_id>/remove", methods=["GET"])
def remove_car(car_id):
    pass

@bp.route("/<int:car_id>/report")
def report_car_with_issue(car_id):
    pass



@bp.route("/admintalk")
def admin_talk():
    a = AdminTalk()
    return a.test()