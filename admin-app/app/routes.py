from flask import request, render_template, redirect, url_for, session
from .main import app
from .services.CarService import CarService
from .services.BookingService import BookingService


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print (request.form.get('username'))
    return render_template('login.html')


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