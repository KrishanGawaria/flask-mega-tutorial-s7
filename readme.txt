Section 4:

* In config.py, following configuration variables are set :
	# The 'SQLALCHEMY_DATABASE_URI' is automatically used by the database for path where the 
	# data is to be stored. (location of the application's database)
	
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')

	# The SQLALCHEMY_TRACK_MODIFICATIONS configuration option is set to False 
	# to disable a feature of Flask-SQLAlchemy that I do not need, which is to 
	# signal the application every time a change is about to be made in the database.
	
	SQLALCHEMY_TRACK_MODIFICATIONS = False

* In __init__.py :

	from flask_sqlalchemy import flask_sqlalchemy 
	# Using this we create below a db variable which represents database

	from flash_migrate import Migrate 
	# Using this we create below a migrate variable

	db = SQLAlchemy(app) # Now, db object represents the database.
	migrate = Migrate(app, db) # Now migrate represents the migration engine


	from app import routes, models # We now import models which defines the structure of the database.



* Database Models:
	The data that will be stored in the database will be represented by a collection of classes, usually called database models. The ORM layer within SQLAlchemy will do the translations required to map objects created from these classes into rows in the proper database tables.

* All the database models(in the form of classes) are created in file app/models.py
	e.g.
	from app import db	# We created this variable in __init__.py

	class User(db.Model):	# Every model we need to inherit from db.Models
		id = db.Column(db.Integer, primary_key=True)
		username = db.Column(db.String(64), index=True, unique=True)
		email = db.Column(db.String(120), index=True, unique=True)
		password_hash = db.Column(db.String(128), index=True, unique=True)

		def __repr__(self):
			return "<User {}>".format(self.username) # e.g. <User Krishan> # where Krishan is username

		# The __repr__ method tells Python how to print objects 
		# of this class, which is going to be useful for debugging.


* We need to create a Migration Repository to handle the potential future changes in the 
	structure of database.
	The flask db sub-command is added by Flask-Migrate to manage everything related to database migrations. So let's create the migration repository for microblog by running command:
	 
	 flask db init

	 Now a new folder 'migrations' is created at top-level directory (i.e. in microblog folder)

* Everytime we make any change in the structure of database (i.e. any change in the modules which
	we create in app/models.py), we need to create database migration by running command:

	flask db migrate -m "users table added"

* After creating migration, we need to apply/commit it by hitting command:
	flask db upgrade

* After adding Post class into app/models.py :
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



* Queries of Database:
	You may try them in python console. Don't forget these: 
		from app import db, from app.models import User, Post
	
	*	Creating a user and adding it into database is a 3 step process:
			1. u = User(username='kk1', email='kk1.com')
			2. db.session.add(u)
			3. db.session.commit()	

	*	Retrieving all users:
			users = User.query.all()
			for user in users:
				print (user.username)
				print (user.email)

	*	Retrieving user by id
			user = User.query.get(1)	# Retrieve user with id 1

	*	Adding a post
			u = User.query.get(1)
			p = Post(body="this post is nice", author=u)
			db.session.add(p)
			db.session.commit()

	*	Retrieving all posts of a user
			u = User.query.get(1)
			posts = u.posts.all()
			for post in posts:
				print(post.body)

	*	Retrieving all posts with their author
			posts = Post.quert.all()
			for post in posts:
				print(post.body)
				print(post.author.username)

	*	Get all users in reverse alphabetical order
			users = User.query.order_by(User.username.desc()).all()

	*	Deleting all users
			users = User.query.all()
			for user in users:
				db.session.delete(user)

			db.session.commit()	



* Modified microblog.py : 
	from app import app, db
	from app.models import User, Post

	@app.shell_context_processor
	def make_shell_context():
		return {'db': db, 'User': User, 'Post': Post}

	# Every time we start python interpreter, we need to import db, User and Post.
	# The above function imports automatically the above import varables in flask shell.
	# To start flask shell, hit command flask shell
