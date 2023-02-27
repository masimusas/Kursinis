from flask_wtf import FlaskForm
import app
import re
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from wtforms import SubmitField, StringField, PasswordField, EmailField
from flask_login import current_user


class UzklausosAtnaujinimoForma(FlaskForm):
    email = StringField('El. paštas', validators=[DataRequired(), Email()], render_kw={"placeholder": "Elektroninis paštas..."})
    submit = SubmitField('Gauti')
    def validate_email(self, email):
        user = app.User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'Nėra paskyros, registruotos šiuo el. pašto adresu. Registruokitės.')


def utility_password_check(password):

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(
        r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    # overall result
    password_ok = not (
        length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

    return password_ok

class PaskyrosAtnaujinimoForma(FlaskForm):
    name = StringField("Vardas", [DataRequired()])
    email = EmailField("El.pastas", [DataRequired()], render_kw={"placeholder": "Elektroninis paštas"})
    submit = SubmitField("Atnaujinti")

    def validate_name(self, name):
        if current_user.name != name.data:  # type: ignore            
            with app.app.app_context():
                user = app.User.query.filter_by(
                    name=name.data).first()
                if user:
                    raise ValidationError(
                        "Sis vardas jau yra musu duomenu bazeje")

    def validate_email(self, email):
        if current_user.email != email.data:  # type: ignore
            with app.app.app_context():
                user = app.User.query.filter_by(
                    email=email.data).first()
                if user:
                    raise ValidationError(
                        "Sis el pastas jau yra musu duomenu bazeje")


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
