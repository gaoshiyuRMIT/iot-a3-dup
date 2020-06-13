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
    newCarVal = carMgr.keepValidFieldsOnly(request.json, throw=True)
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
     # pop 'None' values
    newCarVal = {k: v for k,v in newCarVal.items() if v is not None and v != ""}
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
def assistant_repsonse():
    assistant_query = request.json
    if assistant_query is None:
      return {"fulfillmentText" : "Hmm.. something went wrong."}

    logger.debug(assistant_query["queryResult"]["intent"]["displayName"])
    
    carMgr = CarManager()

    found_match = False

    raw_parameters = assistant_query["queryResult"]["parameters"]

    fields = ["car_id", "year_from", "year_to", "car_model", "body_type", "num_seats_from", 
                "num_seats_to", "car_colour", "cost_hour_from", "cost_hour_to"]
    types = [int, int, int, str, str, int, int, str, float, float]
    # transform/clean search dict
    searchD = {k: (raw_parameters[k] if k in raw_parameters else "") for k in fields}
    searchD = {k: (t(searchD[k]) if searchD[k] else "") for k,t in zip(fields, types)}
    for rangeK in ("year", "num_seats", "cost_hour"):
        fromK = rangeK + "_from"
        toK = rangeK + "_to"
        searchD[rangeK] = [searchD.pop(fromK), searchD.pop(toK)]
        if searchD[rangeK][0] == searchD[rangeK][1]:
            searchD[rangeK] = searchD[rangeK][0]
    searchD = {k: v for k,v in searchD.items() if v}

    logger.debug(searchD)
    matches = carMgr.getMany(searchD)
    if len(matches) <= 0:
      return {"fulfillmentText" : "There's no cars that match that description."}
    else: 
      return {"fulfillmentText" : "Okay. Getting cars matching your description.", "carInfo": matches}

    return {"fulfillmentText" : "Something's gone a bit awry. Please hold."}

