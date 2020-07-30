from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=100, message="Enter a title with more than 5 characters")])
    content = StringField('Content', validators=[DataRequired(), Length(min=10, max=3600,  message="Enter content with more than 10 characters")])
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
  