from flask import Blueprint, request
from app.services.car_service import CarService
from app.services.booking_service import BookingService

bp = Blueprint("cars", __name__, url_prefix="/cars")


@bp.route("/")
def list_cars():
    key = app.config['GOOGLE_API_KEY']
    service = CarService()
    cars = service.searchCars({})
    return render_template("cars.html", cars=cars, key=key)

@bp.route("/", methods=["POST"])
def search_cars():
    # get query from request.form
    pass

@bp.route("/search", methods=["POST"])
def searchCars():
    key = app.config['GOOGLE_API_KEY']
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
    return render_template("cars.html", cars=cars, key=key)



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

@bp.route("/<int:car_id>/map")
def show_car_on_map(car_id):
    pass