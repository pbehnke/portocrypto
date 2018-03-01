from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from jinja2 import FileSystemLoader
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

from config import Config
#from configlocal import Config

# configure application
application = Flask(__name__)

# add config parameters from config.py class
application.config.from_object(Config)

# initializing login instance
login = LoginManager(application)
login.login_view = 'login'

# creating database instance
db = SQLAlchemy(application)

migrate = Migrate(application, db)

# creating mail instance
mail = Mail(application)

# ensure responses aren't cached
if application.config["DEBUG"]:
    @application.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# make jinja look in /templates folder
loader = FileSystemLoader('/templates')

from application import routes, helpers, models
