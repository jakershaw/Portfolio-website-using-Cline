from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ProfileForm(FlaskForm):
    """Edit profile information"""
    profile_photo = FileField('Profile Photo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    bio = TextAreaField('Bio', validators=[Length(max=2000)])
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
    published = BooleanField('Published')
    submit = SubmitField('Save Project')
