from datetime import datetime
from dateutil.tz import tzlocal
import pickle
from flask import request, render_template, redirect, url_for, session, flash
from google.oauth2.credentials import Credentials

from .main import app, client_cred
from .services.CarService import CarService
from .services.BookingService import BookingService
from .services.UserService import UserService
from .errors import APIException
from .utils import CalendarUtil, GAuthUtil


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
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
        return redirect(url_for('index'))
    else:
        flash("Invalid credentials")
        return redirect(url_for('login'))

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
    # call CarService to search for cars, providing search dict
    cars = CarService().searchCars(searchD)
    return render_template("cars.html", cars=cars)


@app.route("/bookings")
def bookings():
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
    if GAuthUtil().getCredential() is None:
        return render_template("addBooking.html", car=car, g_client_id=client_cred["client_id"])
    return render_template("addBooking.html", car=car)


@app.route("/bookings/new", methods=["POST"])
def addBookingPost():
    # clean/transform form data
    data = {}
    data["username"] = session.get("username") or "janedoe1"
    data['car_id'] = int(request.form["car_id"])
    data['date_booking'], data['time_booking'] = request.form['datetime_booking'].split("T")
    data['time_booking'] += ":00"
    data['date_return'], data['time_return'] = request.form['datetime_return'].split("T")
    data['time_return'] += ":00"
    # check for conflicts
    service = BookingService()
    if service.findConflicts(data["car_id"], data["date_booking"], data["date_return"]):
        flash("Timetable conflicts - your chosen time slot conflicts with someone else's booking.")
        return redirect(url_for("addBooking", car_id=data["car_id"]))
    # add a booking
    bk_id = service.addBooking(data)
    flash("Booking successful! Booking ID - {}".format(bk_id))
    # add an event to google calendar
    g_cred = GAuthUtil().getCredential()
    calUtil = CalendarUtil(g_cred)
    data["booking_id"] = bk_id
    event = calUtil.addEvent(data)
    flash(f"Google Calendar event successfully added, link: {event.get('htmlLink')}")
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
    # remove calendar event
    cred = GAuthUtil().getCredential()
    calUtil = CalendarUtil(cred)
    calUtil.deleteEvent(booking)
    return redirect(url_for("bookings"))


@app.route("/tokensignin", methods=["GET", "POST"])
def tokenSignIn():
    token = request.form['accessToken']
    if token == "undefined":
        return "failure: access token is undefined"
    creds = Credentials(
        token, 
        refresh_token=None, 
        client_id=client_cred["client_id"], 
        token_uri=client_cred["token_uri"],
        client_secret=client_cred["client_secret"]
    ) 
    GAuthUtil().setCredential(creds)
    return "success"
