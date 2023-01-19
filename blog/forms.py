"""
Flask Form classes

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Regexp
from blog.utils.settings import images

# This validation technique is based on https://stackoverflow.com/a/67172432/11690953


def FileSizeLimit(max_size_in_mb):
    max_bytes = max_size_in_mb*1024*1024  # Convert MB to bytes

    def file_length_check(form, field):
        if field.data is None:
            return
        if len(field.data.read()) > max_bytes:
            raise ValidationError(
                f"File size must be less than {max_size_in_mb}MB")
        # Reset the file pointer to the beginning of the file
        field.data.seek(0)
    return file_length_check


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp(
        '^[a-z]{6,8}$', message='Your username should be between 6 and 8 characters long, and can only contain lowercase letters.')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'confirm_password', message='Passwords do not match. Try again')])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        from blog.models import User
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                'Username already exist. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class PasswordChangeForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo(
        'confirm_new_password', message='Passwords do not match. Try again')])
    confirm_new_password = PasswordField(
        'Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Upload Picture', validators=[
                        FileSizeLimit(max_size_in_mb=8), FileAllowed(images, 'Image files only!')], default=None)
    submit = SubmitField('Submit Post')


class CommentForm(FlaskForm):
    content = StringField('Your comment', validators=[DataRequired()])
    submit = SubmitField('Submit Comment')


class Deactivation(FlaskForm):
    deactivate = SubmitField('Deactivate Account')


class SettingsForm(FlaskForm):
    avatar = FileField('Upload Avatar', validators=[
                       FileRequired(), FileSizeLimit(max_size_in_mb=2), FileAllowed(images, 'Image files only!')], default=None)
    submit = SubmitField('Save')
