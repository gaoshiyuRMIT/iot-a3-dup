from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from passlib.hash import sha256_crypt
from app.services.user_service import UserService

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/")
def list_users():
    """
    Defines URL/route for displaying users. Retrieves users (stored in 
    cloud database) and routes to html page: '/users'.

    :return: html page to display all users
    :rtype: flask template 
    """
    users = UserService().get_all_users()
    return render_template('users.html', users=users)

@bp.route("/", methods=["POST"])
def search_users():
    """
    Provides logic for filtering/searching displayed users according to 
    their attributes/fields. Retrieves search terms from webpage
    and then matching users (from cloud database) and routes to '/users'.

    :return: html displaying all users matching search terms
    :rtype: flask template
    """
    fields = ["username", "fName", "lName", "email"]
    types = [str, str, str, str]
    #transform and clean dict for search 
    searchDict = {k: request.form[k] for k in fields}
    searchD = {k: v for k,v in searchDict.items() if v}
    # call UserService to search for users, providing search dict
    users = UserService().search_users(searchD)
    return render_template("users.html", users=users)

@bp.route("/<string:username>/update_form", methods=["GET"])
def update_user_page(username):
    """
    Defines URL/route: '/users/username/update' for updating the 
    attributes/fields of a user (except username). Retrieves original 
    user details from cloud database for display and editing.

    :param username: username=primary key for users in user table
    :type username: string
    :return: html for update user page
    :rtype: flask template
    """
    #get user details
    user = UserService().findExistingUser(username)
    #return template with user details attached
    return render_template('updateUser.html', user=user)

@bp.route("/<string:username>/update", methods=["POST"])
def update_user(username):
    """
    Provides logic to retrieve edited details from update user form, and
    then insert in database. If password is changed, hashes password
    and stores hash. Redirects to list of users after update. 

    :param username: username=primary key for user in user table
    :type username: string
    :return: Confirmation message that user has been updated, redirects 
    to user view/search page.
    :rtype: flask template
    """
    #get current user details in order to retain password if needed
    service = UserService()
    data = {
        'fName': request.form['fname'],
        'lName': request.form['lname'],
        'email': request.form['email']
    }
    if request.form["password"] != "":
        data["password"] = sha256_crypt.using(rounds=1000).hash(request.form["password"])
    # call user service to send new user value
    service.update_user(username, data)
    flash(f"successfully updated user: {username}")
    return redirect(url_for("users.list_users"))


@bp.route("/<string:username>/remove", methods=["GET"])
def remove_user(username):
    """
    Defines route to remove user: '/users/username/remove'. Removes 
    user from database and updates user list accordingly. 

    :param username: username=primary key for user in user table
    :type username: string
    :return: updated list of users
    :rtype: flask template
    """
    '''remove user from database and update displays accordingly'''
    #pop up window asking for confirmation
    service = UserService()
    if service.delete_user(username):
        return redirect(url_for('users.list_users'))
    else:
        flash(f"{username} could not be deleted")
        return redirect(url_for('users.list_users'))

@bp.route("/add")
def add_user_page():
    """
    Defines URL/route for add car page, '/cars/add'.

    :return: html for add car form
    :rtype: flask template
    """
    return render_template('addUser.html')

@bp.route("/add", methods=["POST"])
def add_user():
    """
    Provides logic (via POST) to retrieve data entered on the add user 
    page. Confirms entered username is unique, and prompts for different
    username if not. Data is then sent to cloud database to create a new 
    record in user table. 

    :return: confirmation message user was added, redirects to main menu
    :rtype: flask template
    """
    service = UserService()
    username = request.form['username']
    usernameTaken = service.findExistingUser(username)
    if usernameTaken is not None:
        flash(f"Username {username} is already taken. Please try again")
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
            flash(f"Success! User {username} created ")
            return render_template('menu.html')
    