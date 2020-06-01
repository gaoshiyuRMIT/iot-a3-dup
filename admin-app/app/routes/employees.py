from flask import Blueprint, request
from app.services.employee_service import EmployeeService
from app.utils import AuthUtil

bp = Blueprint("employees", __name__, url_prefix="/employees")

@bp.route("/login")
def login_page():
    pass

@bp.route("/login", methods=["POST"])
def login():
    # get input credentials from request.form
    pass

@bp.route("/logout")
def logout():
    pass