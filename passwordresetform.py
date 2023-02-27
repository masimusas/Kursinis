from flask_wtf import FlaskForm
import app
import re
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from wtforms import SubmitField, PasswordField, EmailField
from flask_login import current_user


class ResetRequestForm(FlaskForm):
    email = EmailField("El.pastas", [DataRequired()], render_kw={"placeholder": "Elektroninis paštas.."})
    submit = SubmitField("Gauti")

    def validate_email(self, email):
        with app.app.app_context():
            user = app.User.query.filter_by(email=email.data).first()
            if user is None:
                raise ValidationError("Tokio pasto nera musu duomenu bazeje")


class PasswordResetForm(FlaskForm):
    password = PasswordField("Slaptazodis", [DataRequired()], render_kw={"placeholder": "Naujas slaptažodis"})
    confirm = PasswordField("Pakartokite slaptazodi", [
                                             EqualTo('password', "Slaptazodis turi but toks pats")], render_kw={"placeholder": "Pakartokite slaptažodį"})
    submit = SubmitField("Atnaujinti slaptažodį")
