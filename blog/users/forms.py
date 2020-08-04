from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4, max=12)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[DataRequired(),
                                Length(min=8, max=32)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[ DataRequired(),EqualTo('password',message="Must be equal to the original password!")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username already taken, please choose another one")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "Email already taken, please choose anothher one")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "Hmm, we can't find an account with that email")
        # if user.confirmed is None:
        #     raise ValidationError(
        #         "Unverified email")


class UpdateAccountForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Email()])
    username = StringField('New Username',
                           validators=[DataRequired(),
                                       Length(min=4, max=12)])
    password = PasswordField('New Password') #, validators=[ Length(min=8, max=32)]
    confirm_password = PasswordField('Confirm New Password') #, validators=[EqualTo('password', message="Must be equal to the original password!")]
    picture = FileField('Change Profile Picture', validators =[
        FileAllowed(['jpg', 'png'], message="Invalid file type. Upload JPG or PNG")
    ])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')
 

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if User is None:
            raise ValidationError(
                'No account with that email. Please register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password', validators=[DataRequired(),
                                Length(min=8, max=32)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password',
                    message="Must be equal to the original password!")
        ])
    submit = SubmitField('Reset Password')