from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail
from flask_msearch import Search
from blog.config import Config 
from flask_httpauth import HTTPBasicAuth, HTTPAuth
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail  = Mail()
manager = Manager()
migrate = Migrate()
search = Search()
ma = Marshmallow()
auth = HTTPAuth()
manager.add_command('db', MigrateCommand)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    search.init_app(app)

    # BLUEPRINTS
    from blog.users.routes import users
    from blog.main.routes import main
    from blog.posts.routes import posts
    from blog.API.routes import api

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(api)


    return app