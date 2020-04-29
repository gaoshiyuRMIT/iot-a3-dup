from . import request, url_for, jsonify
from . import app, bkMgr

@app.route("/bookings/search", methods=["GET"])
def bookings():
    # get filter from url args
    filt = {
        "username": request.args.get('username'),
        "status": request.args.get('status')
        # ...
    }
    filt = filter(lambda k: filt[k] is not None, filt)
    bookings = bkMgr.getMany(filt)
    return jsonify(bookings)

    
@app.route("/bookings/<bookingNo>/update", methods=["PUT"])
def updateBooking(bookingNo):
    newBkVal = request.json
    success = bkMgr.updateOne(bookingNo, newBkVal)
    result = {"success": success}
    return jsonify(result)


@app.route("/bookings/add", methods=["POST"])
def addBooking():
    newBkVal = request.json
    bookingNo = bkMgr.addOne(newBkVal)
    return jsonify({"bookingNo": bookingNo})