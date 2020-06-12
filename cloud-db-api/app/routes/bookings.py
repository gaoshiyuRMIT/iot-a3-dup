from . import request, url_for, Blueprint, g
from app.BookingManager import BookingManager
from . import jsonifyResponseData
from app.errors.api_exceptions import MissingKey

bp = Blueprint("bookings", __name__, url_prefix="/bookings")

@bp.route("/search", methods=["POST"])
@jsonifyResponseData
def bookings():
    bkMgr = BookingManager()
    # get filter from url args
    filt = bkMgr.keepValidFieldsOnly(request.json, throw=True)
    filt = {k: v for k,v in filt.items() if v is not None and v != "" and v != []}
    bookings = bkMgr.getMany(filt)
    return bookings

    
@bp.route("/all_with_cars", methods=["GET"])
@jsonifyResponseData
def bookings_w_cars():
    mgr = BookingManager()
    return mgr.getAllWCars()


@bp.route("/<int:bookingNo>/update", methods=["PUT"])
@jsonifyResponseData
def updateBooking(bookingNo):
    bkMgr = BookingManager()
    newBkVal = bkMgr.keepValidFieldsOnly(request.json, throw=True)
    # pop None values
    newBkVal = {k: v for k,v in newBkVal.items() if v is not None and v != ""}
    success = bkMgr.updateOne(bookingNo, newBkVal)
    result = {"success": success}
    return result


@bp.route("/<int:booking_id>")
@jsonifyResponseData
def getBooking(booking_id):
    bkMgr = BookingManager()
    booking = bkMgr.getOne(booking_id)
    if booking is None:
        raise MissingKey("the specified booking_id does not exist")
    return booking


@bp.route("/add", methods=["POST"])
@jsonifyResponseData
def addBooking():
    bkMgr = BookingManager()
    newBkVal = bkMgr.keepValidFieldsOnly(request.json, throw=True)
    # pop primary key
    if "booking_id" in newBkVal:
        newBkVal.pop("booking_id")
    # pop 'None' values
    newBkVal = {k: v for k,v in newBkVal.items() if v is not None and v != ""}
    bookingNo = bkMgr.addOne(newBkVal)
    return {"booking_id": bookingNo}