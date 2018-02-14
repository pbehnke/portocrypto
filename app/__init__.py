from flask import Flask
from flask_session import Session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from jinja2 import FileSystemLoader
from flask_login import LoginManager

# configure application
app = Flask(__name__)

# add config parameters from config.py class
app.config.from_object(Config)

# initializing login instance
login = LoginManager(app)
login.login_view = 'login'

# creating database instance
db = SQLAlchemy(app)

# instance for db migration engine
migrate = Migrate(app, db)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# start session
# Session(app)

# make jinja look in /templates folder
loader = FileSystemLoader('/templates')

from app import routes, helpers, models
