from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CreateDeckForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    submit = SubmitField('Create')


class CreateCardForm(FlaskForm):
    front = StringField(validators=[DataRequired(), Length(
        max=500, message="Max 500 characters.")])
    back = TextAreaField(validators=[DataRequired(), Length(
        max=500, message="Max 500 characters.")])
    submit = SubmitField('Create Card')
