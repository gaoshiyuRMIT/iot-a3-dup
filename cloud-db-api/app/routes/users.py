from . import request, url_for, Blueprint, g
from app.UserManager import UserManager
from app.ActivityManager import ActivityManager
from . import jsonifyResponseData
from app.errors.api_exceptions import MissingKey


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

@bp.route("/add", methods=["POST"])
@jsonifyResponseData
def addUser():
    usMgr = UserManager()
    newUserVal = usMgr.keepValidFieldsOnly(request.json, throw=True)
    # pop None / empty values
    newUserVal = {k:v for k,v in newUserVal.items() if v is not None and v != ""}
    usrPk = usMgr.addOne(newUserVal)
    success = True if usrPk else False
    result = {"success":success}
    return result

@bp.route("/<string:username>/update", methods=["PUT"])
@jsonifyResponseData
def updateUser(username):
    usMgr = UserManager()
    newUserVal = usMgr.keepValidFieldsOnly(request.json, throw=True)
    # pop None / empty values
    newUserVal = {k:v for k,v in newUserVal.items() if v is not None and v != ""}
    success = usMgr.updateOne(username, newUserVal)
    result = {"success":success}
    return result

@bp.route("/search", methods=["POST"])
@jsonifyResponseData
def findUser():
    usMgr = UserManager()
    query = usMgr.keepValidFieldsOnly(request.json, throw=True)
    # ignore empty values
    query = {k:v for k,v in query.items() if v is not None and v != "" and v != []}
    users = usMgr.getMany(query)
    return users

@bp.route("/<string:username>", methods=["DELETE"])
@jsonifyResponseData
def deleteUser(username):
    usMgr = UserManager()
    user = usMgr.getOne(username)
    if user is None:
        raise MissingKey("no user with this username exists")
    success = usMgr.deleteOne(username)
    return {"success": success}

@bp.route("/activity/types", methods=["GET"])
@jsonifyResponseData
def get_activity_types():
    aMgr = ActivityManager()
    return aMgr.get_type_counts()