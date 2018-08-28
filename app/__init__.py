from flask import Flask
from config import Config  

from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 

# The below line includes LoginManager which manages the login functionality of app.
# To include login functionality in app, create a variable below in this file: login=LoginManager(app)
from flask_login import LoginManager # pip install flask-login

app = Flask(__name__) 

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Now login varable includes all the login functionality required.
login = LoginManager(app)	
# usually login variable is used to create user loader function in models.py And to set login_view function below

login.login_view = 'login'	
# Now flask knows that 'login' function has the login form.
# So, wherever we use : @login_required , if the user is not logged in, it will redirect to the 
# 'login' view function

from app import routes, models 

