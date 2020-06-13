from flask import Blueprint, request, render_template, redirect
from flask import url_for, session, flash
from passlib.hash import sha256_crypt
from app.services.employee_service import EmployeeService
from app.utils import AuthUtil

bp = Blueprint("employees", __name__)

@bp.route('/')
def index():
    """
    defines index URL/route: '/'

    :return: html index
    :rtype: flask template
    """
    return render_template('index.html')

@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Defines URL/route for login page: '/login'. Retrieves username and 
    password from form, hashes password to compare with stored hash
    for entered username. If credentials are authorised, directs user to
    landing page depending on thier role (admin/manager/engineer).

    :return: html page (login/homepage) appropriate to user
    :rtype: flask template
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        service = EmployeeService()
        dbEmp = service.find_employee(username)
        if (dbEmp is not None):
            if (sha256_crypt.verify(password, dbEmp['password'])):
                #session.clear()  
                session['username'] = username
                session['fName'] = dbEmp['fName']
                session['loggedIn'] = True
                session['role'] = dbEmp['role']
                # depending on role direct to correct landing page
                if (dbEmp['role'] == 'admin'):
                    return redirect(url_for('employees.menu'))
                elif (dbEmp['role'] == 'manager'):
                    return redirect(url_for('dashboard.dashboard'))
                else:
                    return redirect(url_for(
                                    'cars.list_cars_reported_with_issues'))
            else:
                flash("2 Invalid credentials, please try again")
        else:
            flash("1 Invalid credentials, please try again")
    return render_template('login.html')

@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Defines URL/route for employee registration. Not currently active. 

    :return: html page for registration
    :rtype: flask template
    """
    if request.method == 'POST':
        service = EmployeeService()
        username = request.form['username']
        usernameTaken = service.find_existing_employee(username)
        if usernameTaken is not None:
            flash(f"Username: {username} is already taken. Try again")
            return render_template('register.html')
        else:
            password = request.form['password']
            pwHash = sha256_crypt.using(rounds=1000).hash(password)
            data = {
                'username': username,
                'password': pwHash,
                'fName': request.form['fname'],
                'lNmae': request.form['lname'],
                'email': request.form['email'],
                'role': request.form['role']
            }
            #role must be admin, engineer or manager
            result = service.register_employee(data)
            if result is not None:
                flash("Account created. Please log in.")
                return render_template('login.html')
    return render_template('register.html')

@bp.route("/logout")
def logout():
    """
    Defines route for loggin out: '/logout'. Logs user out by clearing 
    session details, and redirects to login page.

    :return: html for login page
    :rtype: flask template
    """
    session.clear()
    return redirect(url_for('employees.login'))

@bp.route("/menu")
def menu():
    """
    Defines URL/route for main menu: '/menu'. All employees of type admin
    are directed to this page. 

    :return: html for main menu page
    :rtype: flask template
    """
    return render_template('menu.html')