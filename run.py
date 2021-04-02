from app import db, create_app 
from app.blueprints.auth.models import User
from app.blueprints.blog.models import Post 

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post }