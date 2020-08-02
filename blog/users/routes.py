from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import db, bcrypt
from blog.models import User, Post
from blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                              RequestResetForm, ResetPasswordForm)
from blog.users.utils import save_post_picture, save_profile_picture, send_verification_email, send_reset_email
from werkzeug.utils import secure_filename
users = Blueprint('users', __name__)


@users.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        form_picture = form.picture.data
        if form_picture :
            picture_file = save_profile_picture(form_picture)
            if picture_file:
                current_user.profile_image = picture_file
            else:
                flash("Unsupported file type. Please upload .JPG or .PNG")
                return redirect(url_for('users.profile'))
        current_user.username = form.username.data
        current_user.email = form.email.data
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        current_user.password = hashed_pw
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_image = url_for('static',
                            filename='profile_pics/' +
                            current_user.profile_image)
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(per_page=10, page=page)
    return render_template('profile.html',
                           title='Account',
                           profile_image=profile_image,
                           form=form,
                           posts=posts)


@users.route('/profile/<string:username>', methods=['GET', 'POST'])
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('user_posts.html',
                           posts=posts,
                           user=user,
                           )


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            if user.confirmed:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(
                    url_for('main.index'))
            else:
                #todo
                #if a user raises user.confirmed is None: show a link to send verification 
                #on html 
                send_verification_email(user)
                flash(
                    "Verification email has been sent to your email address. ",
                    "info")
                return render_template('login.html', form=form)
        else:
            flash("Wrong credentials, please try again", "error")
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@users.route('/delete/account/<int:user_id>/<string:username>')
@login_required
def deleteaccount(user_id, username):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash("Your account has been successfully deleted", 'success')
        return redirect(url_for('users.login'))
    except:
        flash(
            "Error occured while deleting the account. Try again in a moment",
            'info')
        return redirect(url_for('users.profile'))


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", 'info')
    return redirect(url_for('main.index'))


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            'An email has been sent with instructions to reset your password')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_user_token(token)
    if user is None:
        flash('That token is invalid or has already expired', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Your password has been changed!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form)


@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_pw,
                    confirmed=False)
        db.session.add(user)
        db.session.commit()
        try:
            send_verification_email(user)
            flash("A verification email has been sent to your email id.",
                  'success')
            return redirect(url_for('users.login'))
        except:
            flash(
                "An error occured while sending email. Try again in a moment!",
                'error')
            return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/register/<token>', methods=['POST', 'GET'])
def email_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = User.verify_user_token(token)

    if user is None:
        flash('That token is invalid or has already expired', 'warning')
        return redirect(url_for('users.login'))

    else:
        user.confirmed = True
        db.session.commit()
        flash('Email verified successfully', 'success')
        return redirect(url_for('users.login'))
    form = LoginForm()
    return render_template('login.html', form=form)
