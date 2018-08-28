from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError

from app.models import User

class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	remember_me = BooleanField("Remember Me")
	submit = SubmitField("Sign In")


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