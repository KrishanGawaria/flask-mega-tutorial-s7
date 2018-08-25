Python Section 1:

* To install virtual environment, use command:
	python -m venv venv
	cd venv
	vd Scripts
	activate

* In file app/__init__.py:
	# The directory that contains the __init__.py file is said to be a package.
	# (In this case, since __init__.py is in app directory. So 'app' is a package)

	# When user imports app package, __init__.py executes, and from this(__init__.py) file,
	# all variables can be imported.

	# Also user can import any module (files of extension .py) from app package (e.g. from app import routes)

	from flask import Flask
	app = Flask(__name__) # Now app variable is an instance of Flask	# __name__ is the name of current module/file
	# Because of the line (app = Flask(__name)), flask uses from this location(__name__ i.e. current module/file)
	# to find other folders like 'templates'. So make sure the 'templates' folder should be
	#  in same folders in which this file '__init.py' is there i.e. app package/folder


	from app import routes
	# routes is a file name in app package/folder

	# Since routes module/file is going to import app variable (which is the instance of Flask), therefore
	# the line (from app import routes) is written after creating the app variable.

	# routes.py is a module/file that contains the view functions.
	# View functions are associated to a particular route(URL) through the 
	# decorator: @app.route('URL')

	# To run this application:
	 	# You need to have python script at top level (at parent folder of app package).
			# Let's write the script in the file 'microblog.py'.
			# We need to import the Flask application instance in this file. We can do so by:
				# from app import app
		# In the terminal: hit command: set FLASK_APP=microblog.py (Here we have set FLASK_APP environment variable's value )
		# For unix, the above command would be: export FLASK_APP=microblog.py 
		# Hit command flask run
		# Now the application will start running on port 5000

		# However, the environment variables are not remembered across terminals. So if we close and again open the
			# terminal, we again need to hit the command: set FLASK_APP=microblog.py
		# Install a package: pip install python-dotenv
		# Create a .flaskenv file at top level directory and type in it:
			# FLASK_APP=microblog.py


* In file app/routes.py:
	# Since importing app package executes __init__.py, so we can import any variable
	# inside __init__.py
	from app import app

	# Below, both the routes are mapped to the same view function i.e. index()
	@app.route('/')	# It is a decorator
	@app.route('/index')
	def index():	# It is a view function
		return 'Welcome to the Flask'


	# View functions are associated to a particular route(URL) through the 
	# decorator: @app.route('URL')

* In file microblog.py
	from app import app

* In file .flaskenv
	FLASK_APP=microblog.py