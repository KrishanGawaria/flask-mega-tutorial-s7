from app import db	# We created this variable in __init__.py
from datetime import datetime

# The below package is preinstalled with flask and it handles hashing of passwords.
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin	# it automatically includes properties like: is_authenticated
from app import login  # it is imported to create a user loader function below in this file

class User(UserMixin, db.Model):	# Every model we need to inherit from db.Models
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128), index=True, unique=True)
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	def __repr__(self):
		return "<User {}>".format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
		# generate_password_hash() comes from werkzeug.security that we have imported.
		# It generates the hash of input password

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
		# check_password_hash() comes from werkzeug.security that we have imported.
		# It returns true if the password passed is correct.

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return 'Post : {}'.format(self.body)


# Because Flask-Login knows nothing about databases, it needs the application's 
	# help in loading a user. For that reason, the extension expects that the 
	# application will configure a user loader function, that can be called to 
	# load a user given the ID. 
@login.user_loader	
def load_user(id):
	return User.query.get(int(id))
# The user loader is registered with Flask-Login with the @login.user_loader 
# decorator. The id that Flask-Login passes to the function as an argument is 
# going to be a string, so databases that use numeric IDs need to convert the 
# string to integer as you see above.