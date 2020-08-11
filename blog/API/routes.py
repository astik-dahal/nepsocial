from flask import jsonify, make_response, url_for, request, Blueprint,g
from blog.models import User, Post, UserMixin, PostLike, UserSchema, PostLikeSchema, PostSchema
from blog import bcrypt, db
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from blog import auth
from blog.API.utils import custom_error, verify_password
api = Blueprint('api', __name__)

@api.route('/api/token', methods=['POST'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(3600)
    return jsonify({'token': token.decode('ascii'), 'duration': 3600})



@api.route('/api/users', methods=['GET'])
@auth.login_required
def get_users():
    users_schema = UserSchema(many=True)
    users = User.query.all()
    return jsonify({
        'users': users_schema.dump(users)
    })


@api.route('/api/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    user_schema = UserSchema()
    user = User.query.get(user_id)
    if user is None:
        return custom_error("User doesn't exist", 404)
    return jsonify({
        'user': user_schema.dump(user)
    })


@api.route('/api/users', methods=['POST'])
@auth.login_required
def add_user():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    profile_image = request.json.get('profile_image')
    confirmed = request.json.get('confirmed')

    if request.json is None:
        return custom_error('Missing Arguments', 404)
    if username is None and password is None:
        return custom_error("Missing Arguments", 404)
    if email is None:
        return custom_error("Missing Arguments", 404)

    if User.query.filter_by(username=username).first() is not None:
        return custom_error('User already exists', 404)

    try:
        user = User(
            username=username,
            email=email,
            password=bcrypt.generate_password_hash(password).decode('utf-8'),
            profile_image=profile_image,
            confirmed=confirmed)
        db.session.add(user)
        db.session.commit()
    except:
        return custom_error('An error occured while writing to database.', 404)
    return jsonify({
        'username': user.username,
        'email': user.email
    }), 201, {
        'Location': url_for('api.get_user', user_id=user.id, _external=True)
    }


@api.route('/api/users/<int:user_id>', methods=['PUT'])
@auth.login_required
def update_user(user_id):
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    profile_image = request.json.get('username')
    confirmed = request.json.get('confirmed')
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    if request.json is None:
        return custom_error('Missing Arguments', 404)
    if username is None and password is None:
        return custom_error("Missing Arguments", 404)
    if email is None:
        return custom_error("Missing Arguments", 404)

    user = User.query.get(user_id)
    
    
    if user is None:
        return custom_error('User doesnot exist', 404)
    try:
        user.username = username
        user.email = email
        user.password = hashed_pw
        user.profile_image = profile_image
        user.confirmed = confirmed
        db.session.commit()
    except:
        return custom_error('Error while updating the user', 400)
    return jsonify(
        {
            'success': 'User updated Succesfully'
        }
    ), 201


@api.route('/api/users/<int:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    if request.json is None:
        return custom_error('Empty Response', 404)
    user = User.query.get(user_id)
    if user is None:
        return custom_error('User doesnot Exist', 404)
    try:
        db.session.delete(user)
        db.session.commit()
    except:
        return custom_error('Error while deleting the user', 400)
    return jsonify(
        {
            'success': 'User deleted succesfully'
        }
    ), 201

@api.route('/api/posts', methods=['GET'])
@auth.login_required
def get_posts():
    posts_schema = PostSchema(many = True)
    posts = Post.query.all()
    return jsonify(
        {
            'posts':posts_schema.dump(posts)
        }
    )

@api.route('/api/posts/<int:post_id>', methods=['GET'])
@auth.login_required
def get_post(post_id):
    post = Post.query.get(post_id)
    post_schema = PostSchema()
    if post is None:
        return custom_error('Post not found', 404)
    return jsonify({
       'post':post_schema.dump(post)
    })

@api.route('/api/posts', methods=['POST'])
@auth.login_required
def add_post():
    title = request.json.get('title')
    content = request.json.get('content')
    category = request.json.get('category')
    image_file = request.json.get('image_file')
    user_id = request.json.get('user_id')
    
    if request.json is None:
        return custom_error('Empty Response', 404)
    if title is None and content is None:
        return custom_error("Missing Arguments", 404)
    try: 
        post = Post(title = title, content = content, category = category, image_file = image_file, user_id = user_id)
        db.session.add(post)
        db.session.commit()
    except:
        return custom_error("Error while adding post", 404)
    return jsonify(
        {
            'success': 'Post added Succesfully'
        }
    ), 201
 
@api.route('/api/posts/<int:post_id>', methods=['PUT'])
@auth.login_required
def update_post(post_id):
    
    post = Post.query.get(post_id)
    title = request.json.get('title')
    content = request.json.get('content')
    category = request.json.get('category')
    image_file = request.json.get('image_file')
    
    if request.json is None:
        return custom_error('Empty Response', 404)
    if post is None:
        return custom_error('Post not found', 404)
    if title is None and content is None:
        return custom_error("Missing Arguments", 404)
    try: 
        post.title = title
        post.content = content 
        post.category = category
        post.image_file = image_file
        db.session.commit()
    except:
        return custom_error("Error while updating post", 404)
    return jsonify(
        {
            'success': 'Post updated Succesfully'
        }
    ), 201

    
@api.route('/api/posts/<int:post_id>', methods=['DELETE'])
@auth.login_required
def delete_post(post_id):
    
    post = Post.query.get(post_id)
    
    if request.json is None:
        return custom_error('Empty Response', 404)
    if post is None:
        return custom_error('Post not found', 404)
   
    try: 
        db.session.delete(post)
        db.session.commit()
    except:
        return custom_error("Error while deleting post", 404)
    return jsonify(
        {
            'success': 'Deleted Succesfully'
        }
    ), 201



@api.route('/api/postlikes', methods=['GET'])
@auth.login_required
def postlikes():
    postlikes_schema = PostLikeSchema(many = True)
    postlikes = PostLike.query.all()
    return jsonify(
        {
            'postlikes': postlikes_schema.dump(postlikes)
        }
    )

@api.route('/api/<int:user_id>/<int:post_id>/<action>', methods=['POST'])
@auth.login_required
def post_like(user_id,post_id, action):
    post = Post.query.get(post_id)
    user = User.query.get(user_id)
   
    if post is None:
        return custom_error('Post not found', 404)
    if user is None:
        return custom_error('User not found', 404)
    if action == 'like':
        try:
            user.like_post(post)
            db.session.commit()
            return jsonify({'success': 'post liked'}),201
        except:
            custom_error("Error occured while sending like request", 404)
    if action == 'unlike':
        try:
            user.unlike_post(post)
            db.session.commit()
            return jsonify({'success': 'post unliked'}),201
        except:
            custom_error("Error occured while sending unlike request", 404)
    