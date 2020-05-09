from . import request, url_for, Blueprint, g
from . import bkMgr
from . import jsonifyResponseData

bp = Blueprint("bookings", __name__, url_prefix="/bookings")

@bp.route("/search", methods=["POST"])
@jsonifyResponseData
def bookings():
    # get filter from url args
    filt = bkMgr.keepValidFieldsOnly(request.json, throw=True)
    filt = {k: v for k,v in filt.items() if v is not None and v != ""}
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
    newBkVal = bkMgr.keepValidFieldsOnly(request.json, throw=True)
    # pop primary key
    if "booking_id" in newBkVal:
        newBkVal.pop("booking_id")
    # pop 'None' values
    newBkVal = {k: v for k,v in newBkVal.items() if v is not None and v != ""}
    bookingNo = bkMgr.addOne(newBkVal)
    return {"booking_id": bookingNo}