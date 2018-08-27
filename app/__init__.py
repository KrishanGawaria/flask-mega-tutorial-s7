from flask import Flask
from config import Config  

from flask_sqlalchemy import SQLAlchemy # Using this we create below a db variable which represents database
from flask_migrate import Migrate # Using this we create below a migrate variable

app = Flask(__name__) 

app.config.from_object(Config)

db = SQLAlchemy(app) # Now, db object represents the database.
migrate = Migrate(app, db) # Now migrate represents the migration engine

from app import routes, models # We now import models which defines the structure of the database.

