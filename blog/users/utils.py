import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from blog import mail
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_profile_picture(form_picture):
    if allowed_file(form_picture.filename):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, 'static/profile_pics',
                                    picture_fn)

        output_size = (250, 250)
        i = Image.open(form_picture)
        print("FILENAME: ", form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn


def save_post_picture(form_picture):
    if allowed_file(form_picture.filename):
        random_hex = secrets.token_hex(10)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, 'static/post_pictures',
                                    picture_fn)

        output_size = (700, 700)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn



def send_reset_email(user):
    token = user.get_token(expires_sec = 18000)
    msg = Message('Password Reset Email',
                  sender='testuserdahal@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token = token, _external = True)}

Link is active for next 5 hours.

If you did not make this request, simply discard this email.
'''
    mail.send(msg)


def send_verification_email(user):
    token = user.get_token(expires_sec = 1800)
    msg = Message('Email Verification',
                  sender='testuserdahal@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To verify your email, visit the following link:
{url_for('users.email_token', token = token, _external = True)}

Link is active for next 30 minutes.

If you did not make this request, simply discard this email.
'''
    mail.send(msg)
