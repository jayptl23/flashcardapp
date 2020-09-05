from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class EditCardForm(FlaskForm):
    front = StringField(validators=[DataRequired(), Length(
        max=500, message="Max 500 characters.")])
    back = TextAreaField(validators=[DataRequired(), Length(
        max=500, message="Max 500 characters.")])
    submit = SubmitField('Update')
