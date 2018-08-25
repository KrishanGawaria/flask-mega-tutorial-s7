Python Flask Section 2:

*	All the templates (.html) files are stored in the 'templates' directory to be created
	in the same folder in which lies '__init__.py' file.

*	The operation that converts a template into a complete HTML page is called rendering. To render the template I had to import 	a function that comes with the Flask framework called render_template(). This function takes a template filename and a 			variable list of template arguments and returns the same template, but with all the placeholders in it replaced with actual 	values.

	The render_template() function invokes the Jinja2 template engine that comes bundled with the Flask framework. Jinja2 substitutes {{ ... }} blocks with the corresponding values, given by the arguments provided in the render_template() call.

*	Using if else in templates:
	<head>
      {% if title %}
      <title>{{ title }} - Microblog</title>
      {% else %}
      <title>Welcome to Microblog</title>
      {% endif %}
    </head>

*	Using for loop in templates:
	{% for post in posts %}
    	<div><p>{{ post.author.username }} says: <b>{{ post.body }}</b></p></div>
    {% endfor %}

*	Extending one template from another:
	
	'base.html'
		
		<html>
		    <head>
		      {% if title %}
		      <title>{{ title }} - Microblog</title>
		      {% else %}
		      <title>Welcome to Microblog</title>
		      {% endif %}
		    </head>
		    <body>
		        <div>Microblog: <a href="/index">Home</a></div>
		        <hr>
		        {% block content %}{% endblock %}
		    </body>
		</html>

	'index.html'

		{% extends 'base.html' %}

		{% block content%}
			<h1>Hi, {{ user.username }}!</h1>
		    {% for post in posts %}
		    	<div><p>{{ post.author.username }} says: <b>{{ post.body }}</b></p></div>
		    {% endfor %}
		{% endblock %}
