from blog import create_app, db
from blog.models import User, Post
app = create_app()

if __name__ == '__main__':
    app.run()
    
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}