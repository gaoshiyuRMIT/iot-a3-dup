from . import request, url_for, Blueprint, g
from app.UserManager import UserManager
from . import jsonifyResponseData


bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/register", methods=["POST"])
@jsonifyResponseData
def register():
    usMgr = UserManager()
    newUserVal = request.json
    success = usMgr.addOne(newUserVal)
    result = {"success": success}
    return result


@bp.route("/search", methods=["POST"])
@jsonifyResponseData
def users():
    # not implemented
    usMgr = UserManager()
    return usMgr.getMany({})

@bp.route("/login", methods=["POST"])
@jsonifyResponseData
def login():
    usMgr = UserManager()
    username, password = map(request.json.get, ("username", "password"))
    one = usMgr.getOne(username)
    result = {"success": False, "fname": ""}
    if one is not None and one["password"] == password:
        result["success"] = True
        result["fname"] = one.get("fName", "")
    return result
