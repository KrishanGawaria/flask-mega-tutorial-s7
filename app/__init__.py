from flask import Flask
from config import Config # importing Config class from config.py 

app = Flask(__name__) 

app.config.from_object(Config)	# Telling flask to use configuration variables

from app import routes
