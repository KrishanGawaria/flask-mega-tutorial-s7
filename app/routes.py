from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from app.forms import RegistrationForm

from flask_login import current_user, login_user, logout_user
 

from flask_login import login_required


from flask import request
from werkzeug.urls import url_parse

from app.models import User


from app import db

from datetime import datetime
from app.forms import EditProfileForm


@app.route('/')	
@app.route('/index')
@login_required 
def index():	
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

	return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
	
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()

		if user is None or not user.check_password(form.password.data):
			flash("Invalid username or password")
			return redirect(url_for('login'))
    	
    	
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')	# fetching value of next from : /login?next=/index.
		if not next_page or url_parse(next_page).netloc!='':
			return redirect(url_for('index'))
		return redirect(next_page)
  
	return render_template('login.html', title='SignIn', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))



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


# Profile page
@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]

	return render_template('user.html', user=user, posts=posts)


# Edit Profile route
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


# The below code executes before any request to server is made
	# This is done so as to capture the time when the user makes a request
	# and assign that time to his last_seen
@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

# If you are wondering why there is no db.session.add() before the commit, 
# consider that when you reference current_user, Flask-Login will invoke 
# the user loader callback function, which will run a database query that will 
# put the target user in the database session. So you can add the user again in 
# this function, but it is not necessary because it is already there.