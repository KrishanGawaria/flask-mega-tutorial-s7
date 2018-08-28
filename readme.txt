* Password Hashing
	It's not a good habit of storing password in the database. If the database gets compromised,
	user's password is still unknown to the hacker. Hasing of password is irreversible process.

	Werkzeug:

	This is the package that implements password hashing in flask. It gets automatically included
	when we install flask. 

	*	Generating Password Hash : 

		from werkzeug.security import generate_password_hash
		
		hash = generate_password_hash('input password')

			Now, hash variable contains the hash of the 'input password'. And it can be stored
			in the database.

	*	Check Password (check_password_hash)

		from werkzeug.security import check_password_hash

		check_password_hash(hash, 'input password')	# return True or False



* Flask Login:

 	flask-login extension manages the user logged-in state, so that for example users can log in to the application and then navigate to different pages while the application "remembers" that the user is logged in. It also provides the "remember me" functionality that allows users to remain logged in even after closing the browser window.

 	pip install flask-login

 	As with other extensions, Flask-Login needs to be created and initialized right after the application instance in app/__init__.py. This is how this extension is initialized:

 		from flask_login import LoginManager
 		login = LoginManager(app)


 * There are four important properties used with current_user(current_user is imported from 	
  		flask_login)

  		is_authenticated: a property that is True if the user has valid credentials or False otherwise.
		is_active: a property that is True if the user's account is active or False otherwise.
		is_anonymous: a property that is False for regular users, and True for a special, anonymous user.
		get_id(): a method that returns a unique identifier for the user as a string (unicode, if using Python 2).


		These properties can be included by inheriting the User model from UserMixin class :
		app/models.py:
			# ...
			from flask_login import UserMixin

			class User(UserMixin, db.Model):
			    # ...


* Loader function:
		Because Flask-Login knows nothing about databases, it needs the application's help in loading a user. For that reason, the extension expects that the application will configure a user loader function, that can be called to load a user given the ID. This function can be added in the app/models.py module:

		app/models.py: Flask-Login user loader function

		from app import login
		# ...

		@login.user_loader
		def load_user(id):
		    return User.query.get(int(id))


* filter_by() function : It gives the certain data from database based on the conditions specified 
	in this function.

	e.g. User.query.filter_by(username='krishan').first()
	# It would return the user having username 'krishan'


* Login logic(route) in app/routes.py :

	from flask_login import current_user, login_user
	# current_user is a variable that has information about current user OR on this variable we can
		# use properties like is_authenticated. current_user can be accessed in .html files also
	# login_user is a function which is used to log the users in. 

	@app.route('/login', methods=['GET', 'POST'])
	def login():
		# Checking whether the user is already logged or not.
		# current_user is a special variable imported from flask_login which has info about current user.
		# We can use properties on current_user like is_authenticated which comes from UserMixin class
		if current_user.is_authenticated:
			return redirect(url_for('index'))

		form = LoginForm()
		if form.validate_on_submit():
			user = User.query.filter_by(username=form.username.data).first()

			if user is None or not user.check_password(form.password.data):
				flash("Invalid username or password")
				return redirect(url_for('login'))
	    	
	    	# login_user() is a method that comes from flask_login and it is used to log the user in.
	    	# login_user() also has one special variable: 'remember'.
	    	# If it's value is True, the flask will keep the user logged in even after browser is
	    	#   closed and opened again. 
	    	login_user(user, remember=form.remember_me.data)
	    	return redirect(url_for('index'))

	    return render_template('login.html', title='SignIn', form=form)


* Logging user out:
	from flask_login import logout_user
	logout_user()


* Modified base.html : Provided the link to 'logout' route
	current_user.is_anonymous is true when user is not logged in



* Requiring users to Log in :

	For this feature to be implemented, Flask-Login needs to know what is the view function that handles logins. This can be added in app/__init__.py:

	# ...
		login = LoginManager(app)
		login.login_view = 'login'

		# Now flask knows that 'login' function has the login form.
		# So, wherever we use : @login_required , if the user is not logged in, 
		# it will redirect to the 'login' view function

* In routes.py

	from flask_login import login_required

	@login_required		# Use it before any view function for which authentication is compulsory. 
	def index():
		# ...


* Capturing the previous url from which the user was forcefully redirected to login form, so that
	after getting logged in, the user can be redirected back to the same previous url.

	 If the user navigates to /index, for example, the @login_required decorator will intercept the request and respond with a redirect to /login, but it will add a query string argument to this URL, making the complete redirect URL /login?next=/index. The next query string argument is set to the original URL, so the application can use that to redirect back after login.

	 To fetch the previous url, in routes.py:

	 # The below two packages are used to extract the query string from url
    	# (to extract the previous url from where user was redirected to login form)

		from flask import request
		from werkzeug.urls import url_parse

		in def('login')
		# ...
		next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        # ...

        Three thing happen above:
        * If the login URL does not have a next argument, then the user is redirected to the index  page.
		* If the login URL includes a next argument that is set to a relative path (or in other words, a URL without the domain portion), then the user is redirected to that URL.
		* If the login URL includes a next argument that is set to a full URL that includes a domain name, then the user is redirected to the index page.



* Adding RegisterForm class in the forms.py :

	from wtforms.validators import DataRequired, EqualTo, Email, ValidationError

	class RegistrationForm(LoginForm):
	username = StringField("Username", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("Register")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please Use a Different Username')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a Different Email Address')

	# I need not call these functions manually. Form will automatically validate the 
	# 	username and email by calling these methods.
	# When you add any methods that match the pattern validate_<field_name>, WTForms 
	# takes those as custom validators and invokes them in addition to the stock validators. 
	# In this case I want to make sure that the username and email address entered by the 
	# user are not already in the database, so these two methods issue database queries 
	# expecting there will be no results. In the event a result exists, a validation error 
	# is triggered by raising ValidationError. The message included as the argument in the 
	# exception will be the message that will be displayed next to the field for the user to see.


* Created templates/register.html

* Created register view function in routes.py: 

	from app import db
	from app.forms import RegistrationForm

	# ...

	@app.route('/register', methods=['GET', 'POST'])
	def register():
	    if current_user.is_authenticated:
	        return redirect(url_for('index'))
	    form = RegistrationForm()
	    if form.validate_on_submit():
	        user = User(username=form.username.data, email=form.email.data)
	        user.set_password(form.password.data)
	        db.session.add(user)
	        db.session.commit()
	        flash('Congratulations, you are now a registered user!')
	        return redirect(url_for('login'))
	    return render_template('register.html', title='Register', form=form)