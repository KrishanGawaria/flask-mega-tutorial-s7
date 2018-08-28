from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from app.forms import RegistrationForm

from flask_login import current_user, login_user, logout_user
# current_user is a variable that has information about current user OR on this variable we can
	# use properties like is_authenticated
# login_user is a function which is used to log the users in.
# logout_user is a function which is used to log the users out. 

from flask_login import login_required # for @login_required

# The below two packages are used to extract the query string from url
    # (to extract the previous url from where user was redirected to login form)
from flask import request
from werkzeug.urls import url_parse

from app.models import User

# used in register view function
from app import db


@app.route('/')	# It is a decorator
@app.route('/index')
@login_required # if user is not logged in, it will redirect it to 'login' function as defined in __init__.py
def index():	# It is a view function
	user = {'username' : 'Krishan'}
	posts = [
		{
			'author' : {'username' : 'Krishan'},
			'body' : 'This is Krishan' 
		}, 
		{
			'author' : {'username' : 'Rishabh'},
			'body' : 'This is Rishabh'
		}
	]

	# No need to pass user to the template. current_user variable can be accessed in any template
	return render_template('index.html', title='Home', posts=posts)


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
		next_page = request.args.get('next')	# fetching value of next from : /login?next=/index.
		if not next_page or url_parse(next_page).netloc!='':
			return redirect(url_for('index'))
		return redirect(next_page)
  #   	Three things are happening above:
  #   	* If the login URL does not have a next argument, then the user is redirected to the index page.
		# * If the login URL includes a next argument that is set to a relative path (or in other words, a URL 
		# 	without the domain portion), then the user is redirected to that URL.
		# * If the login URL includes a next argument that is set to a full URL that includes a domain name,
 	# 		then the user is redirected to the index page.
	return render_template('login.html', title='SignIn', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


# Registration means to insert the user details in User database
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = RegistrationForm()
	if form.validate_on_submit():
		u = User(username=form.username.data, email=form.email.data)
		u.set_password(form.password.data)
		db.session.add(u)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))

	return render_template('register.html', title='Register', form=form)




