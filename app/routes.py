# Since importing app package executes __init__.py, so we can import any variable
# inside __init__.py
from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm


@app.route('/')	# It is a decorator
@app.route('/index')
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
	return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()	# from app.forms import LoginForm
    if form.validate_on_submit():	# It returns false if user hits a post request from form
        # The below line generates a flash message (from flask import flash)
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))	# from flask import url_for
    return render_template('login.html', title='Sign In', form=form)


