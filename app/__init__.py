# Flask uses Python's logging package to write its logs, and this package already has 
# the ability to send logs by email. All I need to do to get emails sent out on errors 
# is to add a SMTPHandler instance to the Flask logger object, which is app.logger:
import logging
from logging.handlers import SMTPHandler

# To enable a file based log another handler, this time of type RotatingFileHandler, 
   # needs to be attached to the application logger, in a similar way to the email handler.
from logging.handlers import RotatingFileHandler
import os

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

login = LoginManager(app)	

login.login_view = 'login'	


from app import routes, models, errors


# Sending email
if not app.debug:	# this code executes only when set FLASK_DEBUG=0
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        	print("\n\n\n"+app.config['MAIL_USERNAME'])
        	print("\n\n\n"+app.config['MAIL_PASSWORD'])
        	auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


    # Creating file of the logs
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')



