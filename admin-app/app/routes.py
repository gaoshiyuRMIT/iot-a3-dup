from flask import request, render_template
from .main import app
from .services.CarService import CarService

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print (request.form.get('username'))
    return render_template('login.html')


# just to test that the restful api is connected
@app.route("/cars")
def getAvailableCars():
    service = CarService()
    cars = service.getAllAvailableCars()
    return render_template("index.html", cars=cars)