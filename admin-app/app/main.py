from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from config import Config


app = Flask(__name__)
app.config["RESTFUL_API_ENDPOINT"] = "http://127.0.0.1:6543"
app.config.from_object(Config)

bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template("base.html")

from .routes import cars_bp, employees_bp, users_bp, dashboard_bp

app.register_blueprint(cars_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(users_bp)
app.register_blueprint(dashboard_bp)


