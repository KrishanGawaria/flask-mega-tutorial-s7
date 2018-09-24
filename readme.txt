Section 7:

* There is a bug in this application until now.
	* Make two users. Login from one user.
	* Go to edit profile.
	* Change the username of logged in user to that of other registerd user.
	* This will throw an error page because in the models, in User class,
	  	for username, unique=true.
	* This error is not handled until now.


* Setting debug mode in flask:
	set FLASK_DEBUG=1 // Debug mode is ON now
	set FLASK_DEBUG=0 // Debug mode is off now

	Now if you run the application again while debug mode is ON, try to throw same
	error. Now the error page is more detailed.



* Custom Error Pages: app/errors.py

	# Flask provides a mechanism for an application to install its own error pages, so
	 that
	# your users don't have to see the plain and boring default ones. As an example, let's
	# define custom error pages for the HTTP errors 404 and 500, the two most common ones.
	# Defining pages for other errors works in the same way.

	# To declare a custom error handler, the @errorhandler decorator is used.
	# I'm going to put my error handlers in a new app/errors.py module.

		from flask import render_template
		from app import app, db

		@app.errorhandler(404)
		def not_found_error(error):
		    return render_template('404.html'), 404

		@app.errorhandler(500)	# It is invoked when any database error is there
		def internal_error(error):
		    db.session.rollback()
		    return render_template('500.html'), 500



	# To get these error handlers registered with Flask, I need to import the new
	   app/errors.py module after the application instance is created in __init__.py:

	   	from app import routes, models, errors


	# Created templates\404.html and templates\500.html


	# Now set FLASK_DEBUG=0 ,and run the app. Try to produce the same bug.
		You will get 404.html and 500.html



# Sending Errors by Emails:

	I think it is very important that I take a proactive approach regarding errors. If an
	 error occurs on the production version of the application, I want to know right away.
	  So my first solution is going to be to configure Flask to send me an email
	  immediately after an error, with the stack trace of the error in the email body.

	The first step is to add the email server details to the configuration file:

	config.py:

		class Config(object):

		    # ...

		    MAIL_SERVER = os.environ.get('MAIL_SERVER')
		    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
		    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
		    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
		    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
		    ADMINS = ['your-email@example.com'] # To this list of mails, email will be sent



	Flask uses Python's logging package to write its logs, and this package already has
	 the ability to send logs by email. All I need to do to get emails sent out on errors
	 is to add a SMTPHandler instance to the Flask logger object, which is app.logger:
	__init__.py:

		import logging
		from logging.handlers import SMTPHandler

		# ...

		if not app.debug: 	# this code executes only when set FLASK_DEBUG=0
		    if app.config['MAIL_SERVER']:
		        auth = None
		        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
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



	There are two approaches to test this feature. The easiest one is to use the SMTP
	 debugging server from Python. This is a fake email server that accepts emails, but
	  instead of sending them, it prints them to the console. To run this server, open a
	  second terminal session and run the following command on it:

	(venv) $ python -m smtpd -n -c DebuggingServer localhost:8025

	Leave the debugging SMTP server running and go back to your first terminal and

	set MAIL_SERVER=localhost
	set MAIL_PORT=8025

	in the environment (use set instead of export if you are using Microsoft Windows).
	 Make sure the FLASK_DEBUG variable is set to 0 or not set at all, since the
	 application will not send emails in debug mode. Run the application and trigger the
	 SQLAlchemy error one more time to see how the terminal session running the fake email
	  server shows an email with the full stack trace of the error.



	A second testing approach for this feature is to configure a real email server. Below
	 is the configuration to use your Gmail account's email server:

		export MAIL_SERVER=smtp.googlemail.com
		export MAIL_PORT=587
		export MAIL_USE_TLS=1
		export MAIL_USERNAME=ice.effort
		export MAIL_PASSWORD=**********

		NOTE: 1. MCAfee should be disabled for this.
          2. It won't work on Dell Corp. (as it accesses the googlemail (gmail))
	If you are using Microsoft Windows, remember to use set instead of export in each of
	 the statements above.

	The security features in your Gmail account may prevent the application from sending
	emails through it unless you explicitly allow "less secure apps" access to your Gmail
	 account. You can read about this here, and if you are concerned about the security of
	  your account, you can create a secondary account that you configure just for testing
	   emails, or you can enable less secure apps only temporarily to run this test and
	   then revert back to the default.




Logging to a File:

	To enable a file based log another handler, this time of type RotatingFileHandler,
	needs to be attached to the application logger, in a similar way to the email handler.

	__init__.py:

		# ...
		from logging.handlers import RotatingFileHandler
		import os

		# ...

		if not app.debug:
		    # ...

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



	I'm writing the log file with name microblog.log in a logs directory, which I create
	 if it doesn't already exist.

	The RotatingFileHandler class is nice because it rotates the logs, ensuring that the
	log files do not grow too large when the application runs for a long time. In this
	case I'm limiting the size of the log file to 10KB, and I'm keeping the last ten log
	files as backup.

	The logging.Formatter class provides custom formatting for the log messages. Since
	these messages are going to a file, I want them to have as much information as
	possible. So I'm using a format that includes the timestamp, the logging level, the
	message and the source file and line number from where the log entry originated.

	To make the logging more useful, I'm also lowering the logging level to the INFO
	category, both in the application logger and the file logger handler. In case you are
	 not familiar with the logging categories, they are DEBUG, INFO, WARNING, ERROR and
	 CRITICAL in increasing order of severity.

	As a first interesting use of the log file, the server writes a line to the logs each
	time it starts. When this application runs on a production server, these log entries
	will tell you when the server was restarted.



* Fixing the bug of duplicate username:

	form.py:

		class EditProfileForm(FlaskForm):
	    username = StringField('Username', validators=[DataRequired()])
	    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
	    submit = SubmitField('Submit')

	    # While creating the object of EditProfileForm, we have to pass the
	   	 # 	current user name because it's constructor accepts it
	    def __init__(self, original_username, *args, **kwargs):
	        super(EditProfileForm, self).__init__(*args, **kwargs)
	        self.original_username = original_username

	    def validate_username(self, username):
	        if username.data != self.original_username:
	            user = User.query.filter_by(username=self.username.data).first()
	            if user is not None:
	                raise ValidationError('Please use a different username.')


	routes.py:

		@app.route('/edit_profile', methods=['GET', 'POST'])
		@login_required
		def edit_profile():
		    form = EditProfileForm(current_user.username)
		    # ...
