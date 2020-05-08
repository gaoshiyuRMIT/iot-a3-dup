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


@bp.route("/login", methods=["POST"])
@jsonifyResponseData
def login():
  
    filt = {
        "username": request.json.get("username"),
        "password": request.json.get("password")
    }
    #lst = usMgr.getMany(filt)
    result = {"success": True}
    return result

