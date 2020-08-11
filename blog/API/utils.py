from blog import bcrypt
from flask import g, make_response, jsonify
from blog.models import User
from blog import auth
#import schemas for data serialization
from blog.models import UserSchema, PostSchema, PostLikeSchema

def custom_error(message, status_code):
    return make_response(jsonify({'error': message}), status_code)

@auth.error_handler
def auth_error(status):
    return "Access Denied", status

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    hashed_pw = bcrypt.generate_password_hash(password)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if user and bcrypt.check_password_hash(hashed_pw, password):
            g.user = user
            return True
        else:
            return False
    else:
        g.user = user
        return True

