from datetime import datetime
from flask import Blueprint, request, redirect, url_for, render_template, current_app, flash
from pushbullet import Pushbullet
from app.services.car_service import CarService
from app.services.booking_service import BookingService
from app.services.admintalk import AdminTalk

bp = Blueprint("cars", __name__, url_prefix="/cars")

@bp.route("/")
def list_cars():
    """
    Defines URL/route for displaying cars. Retrieves cars (stored in 
    cloud database) and routes to html page: '/cars'.

    :return: html page to display all cars
    :rtype: flask template 
    """
    key = current_app.config['GOOGLE_API_KEY']
    service = CarService()
    cars = service.search_cars({})
    return render_template("cars.html", cars=cars, key=key)

@bp.route("/reported")
def list_cars_reported_with_issues():
    """
    Defines URL/route for cars with reported issues. Retrieves cars 
    (stored in cloud database) with the status 'hasIssue',
    and routes to appropriate html page '/cars/reported'. Cars are 
    assigned this status when they need an engineer to fix them. 

    :return: html page displaying all cars with status 'hasIssue'
    :rtype: flask template
    """
    cars = CarService().search_cars({"car_status": "hasIssue"})
    pb_channel = current_app.config.get("PUSHBULLET_CHANNEL", "")
    return render_template("reported_cars.html", cars=cars, 
                            pb_channel=pb_channel)

@bp.route("/", methods=["POST"])
def search_cars():
    """
    Provides logic for filtering/searching displayed cars according to 
    their attributes/fields. Retrieves search terms from webpage
    and then matching cars (from cloud database) and routes to '/cars'.

    :return: html displaying all cars matching search terms
    :rtype: flask template
    """
    key = current_app.config['GOOGLE_API_KEY']
    fields = ["car_id", "year_from", "year_to", "car_model", "body_type", 
              "num_seats_from", "num_seats_to", "car_colour", 
              "cost_hour_from", "cost_hour_to"]
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
    """
    Display car location according to passed car ID (via URL)
    and displays car on map utilising google api. 
    Routes to '/cars/carID/map'. 

    :param car_id: ID/primary key of cars in car table
    :type car_id: int
    :return: html displaying car location matching car ID
    :rtype: flask template
    """
    car = CarService().get_car(car_id)
    key = current_app.config['GOOGLE_API_KEY']
    return render_template("map.html", key=key, car=car, 
                            back_to=request.args.get("back_to"))

@bp.route("/add")
def add_car_page():
    """
    Defines URL/route for add car page, '/cars/add'.

    :return: html for add car form
    :rtype: flask template
    """
    return render_template("addCar.html")

@bp.route("/add", methods=["POST"])
def add_car():
    """Provides logic (via POST) to retrieve data entered by user on 
    the add car page and sends this data to database.

    :return: confirmation message of car being added and redirects user 
    to main menu
    :rtype: flask template
    """
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
    """
    Defines URL/route: '/cars/car ID/bookings' and retrieves booking 
    history for car associated with Car ID, to display rental history.

    :param car_id: ID/primary key of cars in car table
    :type car_id: int
    :return: html for rental history of car
    :rtype: flask template
    """
    '''display all bookings made for specific car'''
    service = BookingService()
    bookings = service.get_bookings_for_car(car_id)
    return render_template('carHistory.html', car_id=car_id, 
                            bookings=bookings)


@bp.route("/<int:car_id>/update")
def update_car_page(car_id):
    """
    Defines URL/route: '/cars/car ID/update' for updating attributes of
    car, stored in database (except car ID). 

    :param car_id: ID/primary key of cars in car table
    :type car_id: int
    :return: html for update car page
    :rtype: flask template
    """
    #get current car details
    car = CarService().get_car(car_id)
    #return template with car details attached
    return render_template('updateCar.html', car=car)

@bp.route("/<int:car_id>/update", methods=["PUT"])
def update_car(car_id):
    """
    Provides the logic to retrieve car field information from update car
    page and sends to database. Redirects user to main search page for
    cars.

    :param car_id: ID/primary key of cars in car table
    :type car_id: int
    :return: confirmation message that car has been updated and routes 
    to main list of cars
    :rtype: flask template
    """
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
    """
    Defines URL/route to remove car: '/cars/car ID/remove'. Removes car
    from database and updates display accordingly. 

    :param car_id: ID/primary key of cars in car table
    :type car_id: int
    :return: updated list of cars
    :rtype: flask template
    """
    #pop up window asking for confirmation
    service = CarService()
    if service.delete_car(car_id):
        return redirect(url_for('cars.list_cars'))
    else:
        flash(f"Car #{car_id} could not be deleted")
        return redirect(url_for('cars.list_cars'))

@bp.route("/<int:car_id>/report")
def report_car_with_issue(car_id):
    """
    Defines route to report a car as having an issue and send pushbullet 
    notification to engineer alerting them that thier services are required.
    Updates database car status to 'hasIssue'.  

    :param car_id: ID/primary key of cars in car table
    :type car_id: int
    :return: html page listing cars with status of car updated
    :rtype: flask template
    """
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
