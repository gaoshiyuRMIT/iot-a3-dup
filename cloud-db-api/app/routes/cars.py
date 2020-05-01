from . import request, url_for, jsonify, Blueprint, g
from . import carMgr

bp = Blueprint("cars", __name__, url_prefix="/cars")

@bp.route('/search')
def cars():
    # get filters
    filt = {
        'make': request.args.get("make"),
        'body_type': request.args.get("body_type")
    }
    # ignore None values    
    filt = {k:filt[k] for k in filt if filt[k] is not None}
    cars = carMgr.getMany(filt)
    return jsonify({"data": cars})


@bp.route("/<int:carId>/update", methods=["PUT"])
def updateCar(carId):
    newCarVal = request.json
    success = carMgr.updateOne(carId, newCarVal)
    result = {"success": success}
    return jsonify(result)


@bp.route("/add", methods=["POST"])
def addCar():
    newCarVal = request.json
    carId = carMgr.addOne(newCarVal)
    return jsonify({"carId": carId})


