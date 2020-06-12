import logging
from . import request, url_for, Blueprint, g
from app.CarManager import CarManager
from . import jsonifyResponseData
from app.errors.api_exceptions import MissingKey

logger = logging.getLogger(__name__)

bp = Blueprint("cars", __name__, url_prefix="/cars")

@bp.route('/search', methods=["POST"])
@jsonifyResponseData
def cars():
    carMgr = CarManager()
    # get filters
    filt = carMgr.keepValidFieldsOnly(request.json, throw=True)
    # ignore None values
    filt = {k: v for k,v in filt.items() if v is not None and v != "" and v != []}
    cars = carMgr.getMany(filt)
    return cars


@bp.route("/<int:carId>/update", methods=["PUT"])
@jsonifyResponseData
def updateCar(carId):
    carMgr = CarManager()
    newCarVal = request.json
    newCarVal = carMgr.keepValidFieldsOnly(newCarVal)
    # pop 'None' values
    newCarVal = {k: v for k,v in newCarVal.items() if v is not None and v != ""}
    success = carMgr.updateOne(carId, newCarVal)
    result = {"success": success}
    return result


@bp.route("/<int:carId>")
@jsonifyResponseData
def getCar(carId):
    carMgr = CarManager()
    car = carMgr.getOne(carId)
    if car is None:
        raise MissingKey("the specified car_id does not exist")
    return car


@bp.route("/add", methods=["POST"])
@jsonifyResponseData
def addCar():
    carMgr = CarManager()
    # untested
    newCarVal = request.json
    newCarVal = carMgr.keepValidFieldsOnly(newCarVal)
    carId = carMgr.addOne(newCarVal)
    return {"car_id": carId}

@bp.route("/<int:car_id>", methods=["DELETE"])
@jsonifyResponseData
def delete_car(car_id):
    cMgr = CarManager()
    car = cMgr.getOne(car_id)
    if car is None:
        raise MissingKey("no car with this car_id exists")
    success = cMgr.deleteOne(car_id)
    return {"success": success}

@bp.route("/assistant/", methods=["POST", "GET"])
def assistant_test():
    test = request.json

    if test is None:
      return {"fulfillmentText" : "Hmm.. something went wrong."}

    logger.debug(test["queryResult"])

    response = {"fulfillmentText" : "come on plz work"}
    return response

