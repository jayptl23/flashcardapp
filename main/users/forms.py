from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, equal_to, ValidationError
from main.models import User


class RegistrationForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email(
        message="Invalid email.")])
    password = PasswordField(validators=[DataRequired(), Length(
        min=5, message="Need at least 5 characters.")])
    confirmPassword = PasswordField(
        validators=[DataRequired(), equal_to('password', message="Passwords don't match.")])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already in use.")


class LoginForm(FlaskForm):
    email = StringField(
        validators=[DataRequired(), Email(message="Invalid email.")])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Login')
