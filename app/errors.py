# Flask provides a mechanism for an application to install its own error pages, so that 
# your users don't have to see the plain and boring default ones. As an example, let's 
# define custom error pages for the HTTP errors 404 and 500, the two most common ones. 
# Defining pages for other errors works in the same way.

# To declare a custom error handler, the @errorhandler decorator is used. 
# I'm going to put my error handlers in a new app/errors.py module.

from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)	# It is invoked when any database error is there
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500
