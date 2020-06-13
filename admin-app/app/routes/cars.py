from datetime import datetime
from flask import Blueprint, request, redirect, url_for, render_template, current_app, flash
from pushbullet import Pushbullet
from app.services.car_service import CarService
from app.services.booking_service import BookingService
from app.services.admintalk import AdminTalk

bp = Blueprint("cars", __name__, url_prefix="/cars")

@bp.route("/")
def list_cars():
    key = current_app.config['GOOGLE_API_KEY']
    service = CarService()
    cars = service.search_cars({})
    return render_template("cars.html", cars=cars, key=key)

@bp.route("/reported")
def list_cars_reported_with_issues():
    cars = CarService().search_cars({"car_status": "hasIssue"})
    pb_channel = current_app.config.get("PUSHBULLET_CHANNEL", "")
    return render_template("reported_cars.html", cars=cars, pb_channel=pb_channel)

@bp.route("/", methods=["POST"])
def search_cars():
    key = current_app.config['GOOGLE_API_KEY']
    fields = ["car_id", "year_from", "year_to", "car_model", "body_type", "num_seats_from", 
                "num_seats_to", "car_colour", "cost_hour_from", "cost_hour_to"]
    types = [int, int, int, str, str, int, int, str, float, float]
    # transform/clean search dict
    searchD = {k: request.form[k] for k in fields}
    searchD = {k: (t(searchD[k]) if searchD[k] else "") for k,t in zip(fields, types)}
    for rangeK in ("year", "num_seats", "cost_hour"):
        fromK = rangeK + "_from"
        toK = rangeK + "_to"
        searchD[rangeK] = [searchD.pop(fromK), searchD.pop(toK)]
        if searchD[rangeK][0] == searchD[rangeK][1]:
            searchD[rangeK] = searchD[rangeK][0]
    searchD = {k: v for k,v in searchD.items() if v}
    # call CarService to search for cars, providing search dict
    cars = CarService().search_cars(searchD)
    return render_template("cars.html", cars=cars, key=key)

@bp.route("/<int:car_id>/map")
def map(car_id):
    car = CarService().get_car(car_id)
    key = current_app.config['GOOGLE_API_KEY']
    return render_template("map.html", key=key, car=car, back_to=request.args.get("back_to"))

@bp.route("/add")
def add_car_page():
    return render_template("addCar.html")

@bp.route("/add", methods=["POST"])
def add_car():
    # get new car info from request.form
    service = CarService()
    data = {
        'year': request.form['year'],
        'car_model': request.form['car_model'],
        'body_type' : request.form['body_type'],
        'num_seats' : request.form['num_seats'],
        'car_colour' : request.form['car_colour'],
        'cost_hour' : request.form['cost_hour'],
        'latitude' : request.form['latitude'],
        'longitude' : request.form['longitude'],
        'car_status' : "available"
        }
    result = service.add_car(data)
    if result is not None:
        flash("Success! Car created")
        return render_template('menu.html')


@bp.route("/<int:car_id>/bookings")
def rental_history(car_id):
    '''display all bookings made for specific car'''
    service = BookingService()
    bookings = service.get_bookings_for_car(car_id)
    return render_template('carHistory.html', car_id=car_id, bookings=bookings)


@bp.route("/<int:car_id>/update")
def update_car_page(car_id):
    #get current car details
    car = CarService().get_car(car_id)
    #return template with car details attached
    return render_template('updateCar.html', car=car)

@bp.route("/<int:car_id>/update", methods=["PUT"])
def update_car(car_id):
    service = CarService()
    #store data in dict for transmission
    data = {
        'year': request.form['year'],
        'car_model': request.form['car_model'],
        'body_type': request.form['body_type'],
        'num_seats': request.form['num_seats'],
        'car_colour': request.form['car_colour'],
        'cost_hour': request.form['cost_hour'],
        'latitude': request.form['latitude'],
        'longitude': request.form['longitude'],
        'car_status': request.form['car_status']
        }
    result = service.update_car(car_id, data)
    if result is not None:
        flash(f"Success! Car #{car_id} details updated")
        return redirect(url_for('cars.list_cars'))


@bp.route("/<int:car_id>/remove", methods=["GET"])
def remove_car(car_id):
    '''remove car from database and update displays accordingly'''
    #pop up window asking for confirmation
    service = CarService()
    if service.delete_car(car_id):
        return redirect(url_for('cars.list_cars'))
    else:
        flash(f"Car #{car_id} could not be deleted")
        return redirect(url_for('cars.list_cars'))

@bp.route("/<int:car_id>/report")
def report_car_with_issue(car_id):
    car_svc = CarService()
    pb = Pushbullet(current_app.config["PUSHBULLET_KEY"])
    car_channel = [c for c in pb.channels if c.name == current_app.config["PUSHBULLET_CHANNEL"]][0]
    response = car_channel.push_note(f"Car #{car_id} Issues", f"Car #{car_id} is reported with issues at {datetime.now().isoformat()}")
    car_svc.report_car_with_issue(car_id)
    return redirect(url_for("cars.list_cars"))

@bp.route("/admintalk")
def admin_talk():
    a = AdminTalk()
    return a.test()
