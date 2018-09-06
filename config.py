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


	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Configuring the mail server
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['krishan.garg12@gmail.com']	# To this list of mails, email will be sent
