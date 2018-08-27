from app import app, db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Post': Post}

# Every time we start python interpreter, we need to import db, User and Post.
# The above function imports automatically the above import varables in flask shell.
# To start flask shell, hit command flask shell
