from flask_wtf import FlaskForm
from wtforms import (BooleanField, FloatField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import URL, DataRequired


class CafeForm(FlaskForm):
    cafe_name = StringField(label="Cafe Name", validators=[DataRequired()])
    map_url = StringField(
        label="Cafe Location on Google Maps (URL", validators=[DataRequired(), URL()]
    )
    img_url = StringField(
        label="Picture URL of the Cafe", validators=[DataRequired(), URL()]
    )
    location = StringField(
        label="District this Cafe is in", validators=[DataRequired()]
    )
    seats = SelectField(
        label="Number of Seats",
        choices=["0-10", "10-20", "20-30", "30-40", "40-50", "50+"],
    )
    coffee_price = FloatField(
        label="What is the price of their coffee? (Eg: 1.20)",
        validators=[DataRequired()],
    )
    has_toilet = BooleanField(label="Is there washrooms here?")
    has_wifi = BooleanField(label="Does it have wifi?")
    has_sockets = BooleanField(label="Does it have power sockets?")
    can_take_calls = BooleanField(label="Can you take calls here?")
    submit = SubmitField(label="Submit")
