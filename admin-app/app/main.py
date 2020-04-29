from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print (request.form.get('username'))
    return render_template('login.html')


