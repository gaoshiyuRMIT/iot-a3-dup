from flask import request, Blueprint, url_for
from app.decorators import jsonifyResponseData
from app.employee_manager import EmployeeManager
from app.engineer_manager import EngineerManager
from app.errors.api_exceptions import MissingKey

bp = Blueprint("employees", __name__, url_prefix="/employees")

@bp.route("/<string:username>", methods=["GET"])
@jsonifyResponseData
def get_employee(username):
    eMgr = EmployeeManager()
    user = eMgr.getOne(username)
    if user is None:
        raise MissingKey("no employee with this username exists")
    return user

@bp.route("/engineers/<string:username>")
@jsonifyResponseData
def get_engineer(username):
    eng = EngineerManager().getOne(username)
    if eng is None:
        raise MissingKey("Engineer with this username doesn't exist")
    return eng

@bp.route("/engineers/mac/<string:mac_address>")
@jsonifyResponseData
def get_engineer_by_mac_address(mac_address):
    eng = EngineerManager().get_one_by_mac_address(mac_address)
    if eng is None:
        raise MissingKey("Engineer with this mac address doesn't exist")
    return eng
