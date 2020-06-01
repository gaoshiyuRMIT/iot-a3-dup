from flask import request, Blueprint, url_for
from app.decorators import jsonifyResponseData
from app.employee_manager import EmployeeManager
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