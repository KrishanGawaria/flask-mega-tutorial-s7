Section 6 :

* routes.py :
	Created the view function '/user/<username>'


* Created user.html

* Avatars ;
	To request an image for a given user, a URL with the format https://www.gravatar.com/avatar/<hash>, where <hash> is the MD5 hash of the user's email address.

	To generate avatar:

		from hashlib import md5

		'https://www.gravatar.com/avatar/' + md5(b'john@example.com').hexdigest()
		# it would generate : 'https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
		# The above url is the image of avatar which can be put in <img src=''>

		By default the image size returned is 80x80 pixels, but a different size can be requested by adding a s argument to the URL's query string. For example, to obtain my own avatar as a 128x128 pixel image, the URL is https://www.gravatar.com/avatar/729e26a2a2c7ff24a71958d4aa4e5f35?s=128.

		Another interesting argument that can be passed to Gravatar as a query string argument is d, which determines what image Gravatar provides for users that do not have an avatar registered with the service. My favorite is called "identicon", which returns a nice geometric design that is different for every email.


* models.py : Avatars :

	from hashlib import md5

	# ...

	class User(UserMixin, db.Model):
	    # ...
	    def avatar(self, size):
	        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
	        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
	            digest, size)


* subtemplate : _post.html

	I designed the user profile page so that it displays the posts written by the user, along with their avatars. Now I want the index page to also also display posts with a similar layout. I could just copy/paste the portion of the template that deals with the rendering of a post, but that is really not ideal because later if I decide to make changes to this layout I'm going to have to remember to update both templates.

	Instead, I'm going to make a sub-template that just renders one post, and then I'm going to reference it from both the user.html and index.html templates.

	_post.html

		 <table>
	        <tr valign="top">
	            <td><img src="{{ post.author.avatar(36) }}"></td>
	            <td>{{ post.author.username }} says:<br>{{ post.body }}</td>
	        </tr>
	    </table>


* Added last_seen and about_me fields in the User class in models.py

* user.html:
	Displaying last seen and about me


* routes.py:

	# The below code executes before any request to server is made
		# This is done so as to capture the time when the user makes a request
		# and assign that time to his last_seen
	
	@app.before_request
	def before_request():
		if current_user.is_authenticated:
			current_user.last_seen = datetime.utcnow()
			db.session.commit()

	If you are wondering why there is no db.session.add() before the commit, consider that when you reference current_user, Flask-Login will invoke the user loader callback function, which will run a database query that will put the target user in the database session. So you can add the user again in this function, but it is not necessary because it is already there.


* forms.py:
	# Adding the form for profile editor
		
		class EditProfileForm(FlaskForm):
			username = StringField('username', validators=[DataRequired()])
			about_me = StringField('About me', validators=[Length(min=0, max=140)])
			submit = SubmitField('Submit')


* templates/edit_profile.html file created

* routes.py
	Added the view function for edit profile:
	# Edit Profile route
		@app.route('/edit_profile', methods=['GET', 'POST'])
		@login_required
		def edit_profile():
		    form = EditProfileForm()
		    if form.validate_on_submit():
		        current_user.username = form.username.data
		        current_user.about_me = form.about_me.data
		        db.session.commit()
		        flash('Your changes have been saved.')
		        return redirect(url_for('edit_profile'))
		    elif request.method == 'GET':
		        form.username.data = current_user.username
		        form.about_me.data = current_user.about_me
		    return render_template('edit_profile.html', title='Edit Profile', form=form)



* templates\edit_profile.html:

	<!-- Link to edit profile -->
		{% if user == current_user %}
            <p><a href="{{ url_for('edit_profile') }}">Edit your profile</a></p>
        {% endif %}