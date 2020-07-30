from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField,SubmitField, BooleanField, FileField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from blog.models import User 
from blog import bcrypt
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=12)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Must be equal to the original password!")], )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken, please choose another one")
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("Email already taken, please choose anothher one")
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32)])
    remember = BooleanField('Remember Me') 
    submit = SubmitField('Login')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError("Hmm, we can't find an account with that email")
        
     
class UpdateAccountForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Email()])
    username = StringField('New Username', validators=[DataRequired(),Length(min=4, max=12)])
    # password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=32)])
    # confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password', message="Must be equal to the original password!")])
    picture = FileField('Change Profile Picture', validators=[FileAllowed(['jpg', 'png'])
    ])
    submit = SubmitField('Update')
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
        
class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=100, message="Enter a title with more than 5 characters")])
    content = StringField('Content', validators=[DataRequired(), Length(min=10, max=600,  message="Enter content with more than 10 characters")])
    image_file = FileField('Add an image', validators =[
        FileAllowed(['jpg', 'png'])
    ])
    category = SelectField('Post privacy', choices=[('Public', 'Public'),('Private', 'Private')])
    submit = SubmitField('Add Post')
    
    
class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=100, message="Enter a title with more than 5 characters")])
    content = StringField('Content', validators=[DataRequired(), Length(min=10, max=600,  message="Enter content with more than 10 characters")])
    image_file = FileField('Add an image', validators =[
        FileAllowed(['jpg', 'png'])
    ])
    category = SelectField('Post privacy', choices=[('Public', 'Public'),('Private', 'Private')])
    submit = SubmitField('Update Post')
    
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if User is None:
            raise ValidationError('No account with that email. Please register first')
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Must be equal to the original password!")])
    submit = SubmitField('Reset Password')