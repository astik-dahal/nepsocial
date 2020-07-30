import os
import secrets
from PIL import Image
from flask import render_template, redirect, url_for, flash, request
from blog import app, bcrypt, db, mail
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddPostForm, UpdatePostForm, ResetPasswordForm, RequestResetForm
from blog.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from blog import search

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type = int)
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page , per_page = 10)
        return render_template("newsfeed.html", posts=posts)
    else:
        return render_template('index.html')


@app.route('/post/<int:id>')
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)


def contentPreview(content):
    prv_content = (content[:125] + "..") if len(content) > 127 else content
    return prv_content.rsplit()


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            if user.confirmed :
                print("CONFIRMED")
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(
                    url_for('index'))
            else:
                send_verification_email(user)
                flash("An email has been sent to your email address. ", "info")
                return render_template('login.html', form = form)
        elif user is None:
            flash("The user doesnot exist, register now to continue", "warning")
            return redirect(url_for('register'))
        else:
            flash("Wrong credentials, please try again", "error")
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if request.method == "POST":
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.profile_image = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_image = url_for('static',
                            filename='profile_pics/' +
                            current_user.profile_image)
    page = request.args.get('page', 1, type = int)
    user = User.query.filter_by(username = current_user.username).first()
    posts = Post.query.filter_by(author = user).order_by(Post.date_posted.desc()).paginate(per_page = 10, page = page)
    return render_template('profile.html',
                           title='Account',
                           profile_image=profile_image,
                           form=form,
                           posts = posts)

@app.route('/profile/<string:username>', methods=['GET', 'POST'])
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type = int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author = user).order_by(Post.date_posted.desc()).paginate(page = page, per_page = 10)
    return render_template('user_posts.html', posts = posts, user = user, title = "User Post")


@app.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/delete/account/<int:user_id>/<string:username>')
@login_required
def deleteaccount(user_id, username):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash("Your account has been successfully deleted", 'success')
        return redirect(url_for('login'))
    except:
        flash(
            "Error occured while deleting the account. Try again in a moment",
            'info')
        return redirect(url_for('profile'))


def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',
                                picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def save_post_picture(form_picture):
    random_hex = secrets.token_hex(10)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_pictures',
                                picture_fn)

    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/addpost', methods=['GET', 'POST'])
@login_required
def addpost():
    form = AddPostForm()
    if request.method == "POST":
        if form.image_file.data:
            picture_file = save_post_picture(form.image_file.data)
            post = Post(title=form.title.data,
                        content=form.content.data,
                        image_file=picture_file,
                        category=form.category.data,
                        user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))

        post = Post(title=form.title.data,
                    content=form.content.data,
                    category=form.category.data,
                    user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('addpost.html', form=form)


@app.route('/update/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def updatepost(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id == post.author.id:
        form = UpdatePostForm()
        if request.method == 'POST':
            if form.image_file.data:
                picture_file = save_post_picture(form.image_file.data)
                post = Post(title=form.title.data,
                            content=form.content.data,
                            image_file=picture_file,
                            category=form.category.data,
                            user_id=current_user.id)
                db.session.commit()
                flash("Post updated successfully", "success")
                return redirect(url_for('post', id=post_id))

            post = Post(title=form.title.data,
                        content=form.content.data,
                        category=form.category.data,
                        user_id=current_user.id)
            db.session.commit()
            flash("Post updated successfully", "success")
            return redirect(url_for('post', id=post_id))
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
        return render_template('updatepost.html', form=form)
    else:
        return render_template('403.html'), 403


@app.route('/delete/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def deletepost(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id == post.author.id:
        try:
            db.session.delete(post)
            db.session.commit()
            flash("Post deleted successfully", "success")
            return redirect(url_for('index'))
        except:
            flash("Error while deleting the post, try again in a moment.",
                  "error")
            return redirect(url_for('index'))
    else:
        return render_template('403.html'), 403

@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query')
    if query is '':
        return render_template('search.html', users = None, posts = None)
    posts = Post.query.msearch(query, fields=['title', 'content'])
    users = User.query.msearch(query, fields=['username'])

    # user = User.query.filter_by(username  = users.username).first()
    
    # if user is None and posts is None:
    #     return render_template('search.html', users = None, posts = None)
    # if posts is None:
    #     return render_template('search.html', users = users, posts = None)
    # if users is None:
    #     return render_template('search.html', users = None, posts = posts)

    return render_template('search.html', users = users, posts = posts)
    


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", 'info')
    return redirect(url_for('index'))


def send_reset_email(user):
    token =  user.get_reset_token()
    msg = Message('Password Reset Email',
                  sender='testuserdahal@gmail.com', 
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token   = token, _external = True)}

    If you did not make this request, simply discard this email.
'''
    mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            'An email has been sent with instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_user_token(token)
    if user is None:
        flash('That token is invalid or has already expired', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Your password has been changed!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)




@app.route('/register', methods = ['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')
        user = User(username = form.username.data,
                    email = form.email.data,
                    password = hashed_pw,
                    confirmed = False)
        try:
            send_verification_email(user)
            flash("A verification email has been sent to your email id.", 'success')
            return redirect(url_for('login'))
        except: 
            flash("An error occured while sending email. Try again in a moment!", 'error')
            return redirect(url_for('login'))
        flash("A verification email has been sent to your email id.", 'success')
        
    return render_template('register.html', form = form)

@app.route('/register/<token>', methods = ['POST', 'GET'])
def email_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
   
    user = User.verify_user_token(token)
    if user is None:
        flash('That token is invalid or has already expired', 'warning')
        return redirect(url_for('emailverification_request'))
    else:
        user.confirmed = True
        db.session.commit()
        flash('Email is now verified, please login to continue', 'success')
        return redirect(url_for('login'))
    return render_template('login.html', form = form)
 
def send_verification_email (user):
    token =  user.get_verification_token()
    msg = Message('Email Verification',
                  sender='testuserdahal@gmail.com', 
                  recipients=[user.email])
    msg.body = f'''To verify your email, visit the following link:
{url_for('email_token', token = token, _external = True)}

If you did not make this request, simply discard this email.
'''
    try:
        mail.send(msg)
    except:
        return False