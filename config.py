import os

class Config(object):
	# The below SECRET_KEY variable is used by the flask-wtf extension to protect the web forms 
	# againt any nasty attack called CSRF. This variable will be automatically used by the flask-wtf.
	# Only thing we need to do is to tell flask to use the Configuration variables.
	# We do so by typing app.config.from_object(Config) in __init__.py 
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'

