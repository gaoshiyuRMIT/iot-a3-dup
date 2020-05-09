from . import request, url_for, Blueprint, g
from . import bkMgr
from . import jsonifyResponseData
from app.errors.api_exceptions import MissingKey

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
    newBkVal = bkMgr.keepValidFieldsOnly(request.json, throw=True)
    # pop None values
    newBkVal = {k: v for k,v in newBkVal.items() if v is not None and v != ""}
    success = bkMgr.updateOne(bookingNo, newBkVal)
    result = {"success": success}
    return result


@bp.route("/<int:booking_id>")
@jsonifyResponseData
def getBooking(booking_id):
    booking = bkMgr.getOne(booking_id)
    if booking is None:
        raise MissingKey("the specified booking_id does not exist")
    return booking


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