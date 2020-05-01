from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)
app.config["RESTFUL_API_ENDPOINT"] = "http://localhost:6543"
app.config.from_object(Config)

bootstrap = Bootstrap(app)

from .routes import index, login, getAvailableCars
