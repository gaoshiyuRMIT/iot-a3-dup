from . import request, url_for, Blueprint, g
from . import usMgr
from . import jsonifyResponseData


bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/register", methods=["POST"])
@jsonifyResponseData
def register():
    newUserVal = request.json
    success = usMgr.addOne(newUserVal)
    result = {"success": success}
    return result


@bp.route("/search", methods=["POST"])
@jsonifyResponseData
def users():
    return usMgr.getMany({})

@bp.route("/login", methods=["POST"])
@jsonifyResponseData
def login():
    filt = {
        "username": request.json.get("username"),
        "password": request.json.get("password")
    }
    lst = usMgr.getOne(filt)
    # get first name from result if there is one, otherwise just pass back an empty string (so json doesn't crack it)
    name = lst['fName'] if 'fName' in lst != None else ""
    result = {"success": len(lst) > 0, "fname": name}
    return result