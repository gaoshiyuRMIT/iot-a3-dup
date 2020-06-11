from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from passlib.hash import sha256_crypt
from app.services.user_service import UserService

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/")
def list_users():
    users = UserService().get_all_users()
    return render_template('users.html', users=users)


@bp.route("/", methods=["POST"])
def search_users():
    fields = ["username", "fName", "lName", "email"]
    types = [str, str, str, str]
    searchDict = {k: request.form[k] for k in fields}

    # transform/clean search dict
    searchD = {k: request.form[k] for k in fields}
    searchD = {k: (t(searchD[k]) if searchD[k] else "") for k,t in zip(fields, types)}
    for rangeK in ("year", "num_seats", "cost_hour"):
        fromK = rangeK + "_from"
        toK = rangeK + "_to"
        searchD[rangeK] = [searchD.pop(fromK), searchD.pop(toK)]
        if searchD[rangeK][0] == searchD[rangeK][1]:
            searchD[rangeK] = searchD[rangeK][0]
    searchD = {k: v for k,v in searchD.items() if v}
    # call CarService to search for cars, providing search dict
    cars = CarService().searchCars(searchD)
    return render_template("cars.html", cars=cars, key=key)

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
    return render_template('addUser.html')

@bp.route("/add", methods=["POST"])
def add_user():
    service = UserService()
    username = request.form['username']
    usernameTaken = service.find_user(username)
    if usernameTaken is not None:
        flash("Username: " + username + " is already taken. Pleaase try again")
        return render_template('addUser.html')
    else:
        password = request.form['password']
        pwHash = sha256_crypt.using(rounds=1000).hash(password)
        data = {
            'username': username,
            'password': pwHash,
            'fName': request.form['fname'],
            'lNmae': request.form['lname'],
            'email': request.form['email']
        }
        result = service.add_user(data)
        if result is not None:
            flash("User created. Returning to main menu")
            return render_template('menu.html')
    