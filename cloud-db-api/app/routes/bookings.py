from . import request, url_for, jsonify, Blueprint, g
from . import app, bkMgr

bp = Blueprint("bookings", __name__, url_prefix="/bookings")

@bp.route("/search", methods=["GET"])
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

    
@bp.route("/<int:bookingNo>/update", methods=["PUT"])
def updateBooking(bookingNo):
    newBkVal = request.json
    success = bkMgr.updateOne(bookingNo, newBkVal)
    result = {"success": success}
    return jsonify(result)


@bp.route("/add", methods=["POST"])
def addBooking():
    newBkVal = request.json
    bookingNo = bkMgr.addOne(newBkVal)
    return jsonify({"bookingNo": bookingNo})