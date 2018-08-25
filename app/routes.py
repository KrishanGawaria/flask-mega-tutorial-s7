# Since importing app package executes __init__.py, so we can import any variable
# inside __init__.py
from app import app
from flask import render_template

# Below, both the routes are mapped to the same view function i.e. index()
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


# View functions are associated to a particular route(URL) through the 
# decorator: @app.route('URL')