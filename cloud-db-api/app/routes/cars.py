from . import request, url_for, Blueprint, g
from . import carMgr
from . import jsonifyResponseData
from app.errors.api_exceptions import MissingKey

bp = Blueprint("cars", __name__, url_prefix="/cars")

@bp.route('/search', methods=["POST"])
@jsonifyResponseData
def cars():
    # get filters
    filt = carMgr.keepValidFieldsOnly(request.json, throw=True)
    # ignore None values
    filt = {k: v for k,v in filt.items() if v is not None and v != ""}
    cars = carMgr.getMany(filt)
    return cars


@bp.route("/<int:carId>/update", methods=["PUT"])
@jsonifyResponseData
def updateCar(carId):
    newCarVal = request.json
    newCarVal = carMgr.keepValidFieldsOnly(newCarVal)
    # pop 'None' values
    newCarVal = {k: v for k,v in newCarVal.items() if v is not None and len(v) > 0}
    success = carMgr.updateOne(carId, newCarVal)
    result = {"success": success}
    return result


@bp.route("/<int:carId>")
@jsonifyResponseData
def getCar(carId):
    car = carMgr.getOne(carId)
    if car is None:
        raise MissingKey("the specified car_id does not exist")
    return car


@bp.route("/add", methods=["POST"])
@jsonifyResponseData
def addCar():
    # untested
    newCarVal = request.json
    newCarVal = carMgr.keepValidFieldsOnly(newCarVal)
    carId = carMgr.addOne(newCarVal)
    return {"car_id": carId}


