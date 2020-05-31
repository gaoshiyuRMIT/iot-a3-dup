from . import request, url_for, Blueprint, g
from app.UserManager import UserManager
from . import jsonifyResponseData


bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/registerUser", methods=["POST"])
@jsonifyResponseData
def register():
    usMgr = UserManager()
    newUserVal = request.json
    usrPK = usMgr.addOne(newUserVal)
    success = True if usrPK else False
    result = {"success":success}
    return result

@bp.route("/search", methods=["POST"])
@jsonifyResponseData
def findUser():
    usMgr = UserManager()
    # username = request.json.get('username')
    query = usMgr.keepValidFieldsOnly(request.json, throw=True)
    # ignore empty values
    query = {k:v for k,v in query.items() if v is not None and v != "" and v != []}
    users = usMgr.getMany(query)
    return users
