import json
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask_bootstrap import Bootstrap
from config import Config

client_cred = json.load(open("credentials.json", "rb"))["web"]

app = Flask(__name__)
app.config["RESTFUL_API_ENDPOINT"] = "http://localhost:6543"
app.config["PHOTO_FOLDER"] = "datasets"
app.config.from_object(Config)

bootstrap = Bootstrap(app)

from . import routes
