from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail
from flask_msearch import Search
#app initializations
app = Flask(__name__)



#config files
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['confirm_deleted_rows'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = '587'
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
mail  = Mail(app)

# initializing the database
db = SQLAlchemy(app)

#initializing MSEARCH for searching databases
search = Search(app)

# flask migrate app creation
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
 
# bcrypt init
bcrypt = Bcrypt(app)

#http auth
from flask_httpauth import HTTPBasicAuth 
auth = HTTPBasicAuth()

#marshmallow object serializer 
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

# flask login manager
login_manager = LoginManager(app)


#redirecting to login page when user!=loggedin (when redirected by @loginrequired)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from blog import routes, errors, api_routes
