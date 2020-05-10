from flask import request, render_template, redirect, url_for, session, flash
from .main import app
from .services.CarService import CarService
from .services.BookingService import BookingService
from .services.UserService import UserService
from .errors import APIException

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_check', methods=['POST', 'GET'])
def login_check():
    service = UserService()
    isValidUser = service.isValidUser(request.form.get('username'), request.form.get('password'))
    validUser = service.getValidUser(request.form.get('username'), request.form.get('password'))
    if (validUser):
        session['username'] = request.form.get('username')
        session['fName'] = validUser
        session['loggedIn'] = True
    return redirect(url_for('index')) if validUser else redirect(url_for('login', error="Invalid login credentials"))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('loggedIn', None)
    session.pop('fName', None)
    return redirect(url_for('index'))

@app.route("/users")
def users():
    service = UserService()
    users = service.getAllUsers()
    return render_template("users.html", output=users, users=users)

@app.route("/cars")
def cars():
    service = CarService()
    cars = service.getAllAvailableCars()
    return render_template("cars.html", cars=cars)


@app.route("/cars/search", methods=["POST"])
def searchCars():
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
    searchD["car_status"] = "available"
    # call CarService to search for cars, providing search dict
    cars = CarService().searchCars(searchD)
    return render_template("cars.html", cars=cars)


@app.route("/bookings")
def bookings():
    # TODO: modify according to Aspen's implementation of login
    username = session.get("username") or "janedoe1"
    bookings = BookingService().getBookingsForUser(username)
    return render_template("bookings.html", bookings=bookings)

@app.route("/bookings/new", methods=["GET"])
def addBooking():
    car_id = request.args.get("car_id")
    car_id = int(car_id)
    car = None
    try:
        car = CarService().getCar(car_id)
    except APIException as e:
        if e.error_code == "MissingKey":
            return redirect(url_for("cars"))
        raise
    return render_template("addBooking.html", car=car)


@app.route("/bookings/new", methods=["POST"])
def addBookingPost():
    data = {}
    # TODO: modify according to Aspen's implementation of login
    data["username"] = session.get("username") or "janedoe1"
    data['car_id'] = int(request.form["car_id"])
    data['date_booking'], data['time_booking'] = request.form['datetime_booking'].split("T")
    data['time_booking'] += ":00"
    data['date_return'], data['time_return'] = request.form['datetime_return'].split("T")
    data['time_return'] += ":00"
    bk_id = BookingService().addBooking(data)
    CarService().updateCar(data['car_id'], {"car_status": "booked"})
    flash("Booking successful! Booking ID - {}".format(bk_id))
    return redirect(url_for("cars"))

@app.route("/bookings/<int:booking_id>/cancel")
def cancelBooking(booking_id):
    bkService = BookingService()
    booking = None
    try:
        booking = bkService.getBooking(booking_id)
    except APIException as e:
        if e.error_code == "MissingKey":
            flash("No booking with ID {} exists!".format(booking_id))
            return redirect(url_for("bookings"))
    success = bkService.updateBooking(booking_id, {"status": "cancelled"})
    CarService().updateCar(booking["car_id"], {"car_status": "available"})
    flash("Booking {} successfully cancelled!".format(booking_id))
    return redirect(url_for("bookings"))