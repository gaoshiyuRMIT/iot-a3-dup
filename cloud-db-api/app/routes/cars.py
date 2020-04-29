from . import request, url_for, jsonify
from . import app, carMgr

@app.route('/cars/search')
def cars():
    # get filters
    filt = {
        'make': request.args.get("make"),
        'body_type': request.args.get("body_type")
    }
    # ignore None values    
    filt = filter(lambda k: filt[k] is not None, filt)
    cars = carMgr.getMany(filt)
    return jsonify(cars)


@app.route("/cars/<carId>/update", methods=["PUT"])
def updateCar(carId):
    newCarVal = request.json
    success = carMgr.updateOne(carId, newCarVal)
    result = {"success": success}
    return jsonify(result)


@app.route("/cars/add", methods=["POST"])
def addCar():
    newCarVal = request.json
    carId = carMgr.addOne(newCarVal)
    return jsonify({"carId": carId})


