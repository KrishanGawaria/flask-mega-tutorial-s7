from app import db	# We created this variable in __init__.py
from datetime import datetime

class User(db.Model):	# Every model we need to inherit from db.Models
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128), index=True, unique=True)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	 # If I have a user stored in u, the expression u.posts will run a 
	 	# database query that returns all the posts written by that user. 
	 # If I run post.author, it will return the user who wrote that post.
	def __repr__(self):
		return "<User {}>".format(self.username) # e.g. <User Krishan> # where Krishan is username

	# The __repr__ method tells Python how to print objects 
	# of this class, which is going to be useful for debugging.

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return 'Post : {}'.format(self.body)