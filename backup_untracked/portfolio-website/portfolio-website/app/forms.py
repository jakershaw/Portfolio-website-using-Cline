from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ProfileForm(FlaskForm):
    """Edit profile information"""
    display_name = StringField('Display Name', validators=[Length(max=100)])
    bio_header = StringField('Bio Header', validators=[Length(max=200)])
    profile_photo = FileField('Profile Photo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    bio = TextAreaField('Bio', validators=[Length(max=2000)])
    about_text = TextAreaField('About Page Text', validators=[Length(max=5000)])
    email = StringField('Email', validators=[DataRequired(), Length(max=120)])
    linkedin_url = StringField('LinkedIn URL', validators=[Optional(), URL()])
    github_url = StringField('GitHub URL', validators=[Optional(), URL()])
    submit = SubmitField('Update Profile')


class ProjectForm(FlaskForm):
    """Add/edit project"""
    title = StringField('Project Title', validators=[DataRequired(), Length(max=200)])
    description = StringField('Short Description', validators=[DataRequired(), Length(max=500)])
    content = TextAreaField('Project Content (Markdown supported)', validators=[DataRequired()])
    github_url = StringField('GitHub Repository URL', validators=[Optional(), URL()])
    image = FileField('Project Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    content_images = MultipleFileField('Content Images', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    published = BooleanField('Published')
    submit = SubmitField('Save Project')
