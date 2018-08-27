* Created config.py : 
	This file contains all the configuration variables which are automatically used by
	flask. 
	Only thing we need to do is to tell flask to use the Configuration variables.
	We do so by typing app.config.from_object(Config) in __init__.py 

* Added app/forms.py :

	from flask_wtf import FlaskForm
	from wtforms import StringField, PasswordField, BooleanField, SubmitField
	from wtforms.validators import DataRequired

	class LoginForm(FlaskForm):
	    username = StringField('Username', validators=[DataRequired()])
	    password = PasswordField('Password', validators=[DataRequired()])
	    remember_me = BooleanField('Remember Me')
	    submit = SubmitField('Sign In')

* To get the flash messages in html: 
	{%with messages = get_flashed_messages()%}

	{% endwith%}

* To generate flash messages from routes.py file : from flask impost flash
	flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))

* In routes.py :

	@app.route('/login', methods=['GET', 'POST'])
	def login():
	    form = LoginForm()	# from app.forms import LoginForm
	    if form.validate_on_submit():	# It returns false if user hits a post request from form
	        flash('Login requested for user {}, remember_me={}'.format(
	            form.username.data, form.remember_me.data))
	        return redirect(url_for('index')) # from flask import url_for
	    return render_template('login.html', title='Sign In', form=form)
	