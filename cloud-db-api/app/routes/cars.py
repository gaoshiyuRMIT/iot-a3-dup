from . import request, url_for, Blueprint, g
from . import carMgr
from . import jsonifyResponseData

bp = Blueprint("cars", __name__, url_prefix="/cars")

@bp.route('/search')
@jsonifyResponseData
def cars():
    # get filters
    filt = carMgr.keepValidFieldsOnly(request.args)
    # ignore None values    
    filt = {k: filt[k] for k in filt if filt[k] is not None}
    cars = carMgr.getMany(filt)
    return cars


@bp.route("/<int:carId>/update", methods=["PUT"])
@jsonifyResponseData
def updateCar(carId):
    newCarVal = request.json
    newCarVal = carMgr.keepValidFieldsOnly(newCarVal)
    success = carMgr.updateOne(carId, newCarVal)
    result = {"success": success}
    return result


@bp.route("/add", methods=["POST"])
@jsonifyResponseData
def addCar():
    newCarVal = request.json
    newCarVal = carMgr.keepValidFieldsOnly(newCarVal)
    carId = carMgr.addOne(newCarVal)
    return {"car_id": carId}


