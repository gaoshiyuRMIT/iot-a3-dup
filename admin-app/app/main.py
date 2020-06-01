from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config


app = Flask(__name__)
app.config["RESTFUL_API_ENDPOINT"] = "http://127.0.0.1:6543"
app.config.from_object(Config)

bootstrap = Bootstrap(app)

from . import routes
