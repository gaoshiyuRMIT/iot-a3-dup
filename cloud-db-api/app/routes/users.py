from . import request, url_for, jsonify, Blueprint, g
from . import app, usMgr

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/register", methods=["POST"])
def register():
    newUserVal = request.json
    usMgr.addOne(newUserVal)
    result = {"success": 1}
    return jsonify(result)


@bp.route("/login", methods=["POST"])
def login():
    filt = {
        "username": request.json.get("username"),
        "password": request.json.get("password")
    }
    lst = usMgr.getMany(filt)
    result = {"success": 1}
    if len(lst) == 0:
        result = {"success": 0, "error_code": "IncorrectCredentials", 
                "error_message": "the combination of username and password doesn't exist"}
    return jsonify(result)

