from datetime import datetime
from flask import current_app
from blog import db, login_manager,bcrypt, ma

#python object serializer
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

#flask login for easy logging in features
from flask_login import UserMixin

#serializer and token generator
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature,
                           BadTimeSignature, URLSafeTimedSerializer, SignatureExpired)

#for searching the db
from blog import search

#for tokenization
import jwt
#for token authorization
import time


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# creating a model
class User(db.Model, UserMixin):
    __searchable__ = ['username']
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile_image = db.Column(db.String(60), default='default.jpg')
    confirmed = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    liked = db.relationship('PostLike',
                            foreign_keys='PostLike.user_id',
                            backref='user',
                            lazy='dynamic')

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        password_hash = bcrypt.generate_password_hash(password)
        return bcrypt.check_password_hash(password_hash, self.password)


    def get_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_user_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    # implementing authentication based on tokens
    def generate_auth_token(self, expires_in=600):
        return jwt.encode({
            'id': self.id,
            'exp': time.time() + expires_in
        },
                          current_app.config['SECRET_KEY'],
                          algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token,
                              current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return
        return User.query.get(data['id'])

    #like features
    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(PostLike.user_id == self.id,
                                     PostLike.post_id == post.id).count() > 0

    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.profile_image}')"


class Post(db.Model):
    __searchable__ = ['title', 'content']
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(90), nullable=True, default='')
    content = db.Column(db.String(3000), nullable=False)
    # contentPrv = db.Column(db.String(150), nullable=False)
    image_file = db.Column(db.String(60))
    category = db.Column(db.String(20), default='Public')
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.date_posted}', '{self.title}')"


class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# Creating Schema for data serialization:


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True
        load_instance = True


class PostLikeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PostLike
        include_fk = True
        load_instance = True