from wtforms import PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    email = EmailField(validators=[Email()], render_kw={"placeholder": "Elektroninis paštas"})
    password = PasswordField(validators=[ InputRequired(), 
    Length(min=1, max=20)], render_kw={"placeholder": "Slaptažodis"})
    remember_my = BooleanField("Prisiminti mane")
    submit = SubmitField('Prisijunkite ')


