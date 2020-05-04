from . import request, url_for, Blueprint, g
from . import bkMgr
from . import jsonifyResponseData

bp = Blueprint("bookings", __name__, url_prefix="/bookings")

@bp.route("/search", methods=["GET"])
@jsonifyResponseData
def bookings():
    # get filter from url args
    filt = bkMgr.keepValidFieldsOnly(request.args)
    filt = filter(lambda k: filt[k] is not None, filt)
    bookings = bkMgr.getMany(filt)
    return bookings

    
@bp.route("/<int:bookingNo>/update", methods=["PUT"])
@jsonifyResponseData
def updateBooking(bookingNo):
    newBkVal = request.json
    success = bkMgr.updateOne(bookingNo, newBkVal)
    result = {"success": success}
    return result


@bp.route("/add", methods=["POST"])
@jsonifyResponseData
def addBooking():
    newBkVal = request.json
    bookingNo = bkMgr.addOne(newBkVal)
    return {"booking_id": bookingNo}