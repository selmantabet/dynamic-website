from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Regexp


# This validation technique is based on https://stackoverflow.com/a/67172432/11690953
def FileSizeLimit(max_size_in_mb):
    max_bytes = max_size_in_mb*1024*1024  # Convert MB to bytes

    def file_length_check(form, field):
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
    confirm_password = PasswordField('Password', validators=[DataRequired()])
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


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    picture = FileField('Upload Picture', validators=[
                        FileSizeLimit(max_size_in_mb=8)])
    submit = SubmitField('Submit Post')


class CommentForm(FlaskForm):
    content = StringField('Your comment', validators=[DataRequired()])
    submit = SubmitField('Submit Comment')


class Deactivation(FlaskForm):
    # submit = SubmitField('Save')
    deactivate = SubmitField('Deactivate Account')


class SettingsForm(FlaskForm):
    avatar = FileField('Upload Avatar', validators=[
                       DataRequired(), FileSizeLimit(max_size_in_mb=2)])
    submit = SubmitField('Save')
