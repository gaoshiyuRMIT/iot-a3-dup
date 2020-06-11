from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from passlib.hash import sha256_crypt
from app.services.employee_service import EmployeeService
from app.utils import AuthUtil

bp = Blueprint("employees", __name__)

@bp.route('/')
def index():
   return render_template('index.html')

@bp.route("/login", methods=["GET", "POST"])
def login():
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
                # depending on type of employee direct to correct landing page
                if (dbEmp['role'] == 'admin'):
                    return redirect(url_for('employees.menu'))
                elif (dbEmp['role'] == 'manager'):
                    return redirect(url_for('dashboard.dashboard'))
                else:
                    return redirect(url_for('cars.list_cars_reported_with_issues'))
            else:
                flash("Invalid credentials, please try again")
        else:
            flash("Invalid credentials, please try again")
    return render_template('login.html')

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        service = EmployeeService()
        username = request.form['username']
        usernameTaken = service.find_employee(username)
        if usernameTaken is not None:
            flash("Username: " + username + " is already taken. Try again")
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
            result = service.register_employee(data)
            if result is not None:
                flash("Account created. Please log in.")
                return render_template('login.html')
    return render_template('register.html')

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('employees.index'))

@bp.route("/menu")
def menu():
    return render_template('menu.html')


