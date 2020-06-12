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
    #transform and clean dict for search 
    searchDict = {k: request.form[k] for k in fields}
    searchD = {k: v for k,v in searchDict.items() if v}
    # call UserService to search for users, providing search dict
    users = UserService().search_users(searchD)
    return render_template("users.html", users=users)

@bp.route("/<string:username>/update", methods=["GET"])
def update_user_page(username):
    #get user details
    user = UserService().findExistingUser(username)
    #return template with user details attached
    return render_template('updateUser.html', user=user)

@bp.route("/<string:username>/update", methods=["PUT"])
def update_user(username):
    #get current user details in order to retain password if needed
    service = UserService()
    user = service.findExistingUser(username)
    if request.form['password'] is None:
        password = user['password']
    #store data in dict for transmission
    pwHash = sha256_crypt.using(rounds=1000).hash(password)
    data = {
        'username': username,
        'password': pwHash,
        'fName': request.form['fname'],
        'lName': request.form['lname'],
        'email': request.form['email']
    }
    result = service.update_user(username, data)
    if result is not None:
        flash("Success! User details updated")
        return redirect(url_for('users.list_users'))

@bp.route("/<string:username>/remove", methods=["GET"])
def remove_user(username):
    '''remove user from database and update displays accordingly'''
    #pop up window asking for confirmation
    service = UserService()
    if service.delete_user(username):
        return redirect(url_for('users.list_users'))
    else:
        flash("User: " + username + "could not be deleted")
        return redirect(url_for('users.list_users'))

@bp.route("/add")
def add_user_page():
    return render_template('addUser.html')

@bp.route("/add", methods=["POST"])
def add_user():
    service = UserService()
    username = request.form['username']
    usernameTaken = service.findExistingUser(username)
    if usernameTaken is not None:
        flash("Username: " + username + " is already taken. Please try again")
        return render_template('addUser.html')
    else:
        password = request.form['password']
        pwHash = sha256_crypt.using(rounds=1000).hash(password)
        data = {
            'username': username,
            'password': pwHash,
            'fName': request.form['fname'],
            'lName': request.form['lname'],
            'email': request.form['email']
        }
        result = service.add_user(data)
        if result is not None:
            flash("Success! User created ")
            return render_template('menu.html')
    