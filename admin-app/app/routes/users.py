from flask import Blueprint, request
from app.services.user_service import UserService

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/")
def list_users():
    pass

@bp.route("/", methods=["POST"])
def search_users():
    # get query from request.form
    pass

@bp.route("/<string:username>/update", methods=["GET"])
def update_user_page(username):
    pass

@bp.route("/<string:username>/update", methods=["PUT"])
def update_user(username):
    # get changed user info from request.form
    pass

@bp.route("/<string:username>/remove", methods=["GET"])
def remove_user(username):
    pass

@bp.route("/add")
def add_user_page():
    pass

@bp.route("/add", methods=["POST"])
def add_user():
    # get user info to add from request.form
    pass