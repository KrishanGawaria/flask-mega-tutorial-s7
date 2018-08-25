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