import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	# The below SECRET_KEY variable is used by the flask-wtf extension to protect the web forms 
	# againt any nasty attack called CSRF. This variable will be automatically used by the flask-wtf.
	# Only thing we need to do is to tell flask to use the Configuration variables.
	# We do so by typing app.config.from_object(Config) in __init__.py 
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'

	# The 'SQLALCHEMY_DATABASE_URI' is automatically used by the database for path where the 
	# data is to be stored. (location of the application's database)
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')

	# The SQLALCHEMY_TRACK_MODIFICATIONS configuration option is set to False 
	# to disable a feature of Flask-SQLAlchemy that I do not need, which is to 
	# signal the application every time a change is about to be made in the database.
	SQLALCHEMY_TRACK_MODIFICATIONS = False
