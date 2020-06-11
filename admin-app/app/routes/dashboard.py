from collections import Counter
from datetime import timedelta
from flask import Blueprint, request, render_template, jsonify
from app.services.car_service import CarService
from app.services.user_service import UserService
from app.services.booking_service import BookingService

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@bp.route("/data/car_usage")
def car_usage():
    '''number of cars being used each day
    '''
    bk_svc = BookingService()
    bookings = bk_svc.search_bookings({})
    counter = Counter()
    for bk in bookings:
        bk_svc.transform_date(bk)
        curr = bk["date_booking"]
        while curr <= bk["date_return"]:
            date_s = bk_svc.gen_date_str(curr)
            counter[date_s] += 1
            curr += timedelta(days=1)
    data = []
    for k, n in counter.items():
        data.append({"date": k, "n_cars": n})
    return jsonify(data)

@bp.route("/data/revenue")
def rental_revenue():
    '''revenue generated from rental each day
    '''
    bk_svc = BookingService()
    bookings = bk_svc.get_all_with_cars()
    counter = Counter()
    for bk in bookings:
        bk_svc.transform_date(bk)
        bk_svc.transform_time(bk)
        delta = bk["date_return"] - bk["date_booking"] + bk["time_return"] - bk["time_booking"]
        hours = delta.seconds / timedelta(hours=1).seconds
        date_s = bk_svc.gen_date_str(bk["date_return"])
        counter[date_s] += hours * bk["cost_hour"]
    data = []
    for k, n in counter.items():
        data.append({"date": k, "revenue": n})
    data.sort(key=lambda d: d["date"])
    # accumulative
    for i in range(1, len(data)):
        data[i]['revenue'] += data[i-1]["revenue"]
    return jsonify(data)

@bp.route("/data/user_activities")
def user_activities():
    '''# of active users each day
    '''
    type_counts = UserService().get_activity_types()
    return jsonify(type_counts)