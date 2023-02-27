from wtforms import StringField, PasswordField, SubmitField, SelectField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, Email
from flask_wtf import FlaskForm
from app import User, app
import re


def utility_password_check(password):
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[ ?!#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error  # or symbol_error
                       )
    return password_ok

class RegisterForm(FlaskForm):
    name = StringField(validators=[InputRequired(),Length(min=3, max=25)], render_kw={"placeholder": "Vardas"})
    surname = StringField(validators=[InputRequired(),Length(min=4, max=25)], render_kw={"placeholder": "Pavardė"})
    email = EmailField(validators=[Email()], render_kw={
                       "placeholder": "Elektroninis paštas"})
    department = SelectField('Skyrius', choices=[(1, "PVC Gamyba"), (2, "ALU Gamyba"), (3, "Administracija")], validators=[InputRequired()], render_kw={"placeholder": "Skyrius"})
    password = PasswordField(validators=[InputRequired(),Length(min=1, max=25)], render_kw={"placeholder": "Slaptažodis"})
    confirm = PasswordField(validators=[EqualTo('password', 'Slaptažodis nesutampa')], render_kw={"placeholder": "Pakartokite slaptažodį"})
    submit = SubmitField('Registruotis')

    def validate_email(self, email):
        with app.app_context():
            print("hey")
            print(email.data)
            vartotojas = User.query.filter_by(email=email.data).first()
            print(vartotojas)
            if vartotojas:
                raise ValidationError('Šis elektroninio pašto adresas panaudotas. Pasirinkite kitą.')

    def validate_password(self, password):
        tinkamas_slaptazodis = utility_password_check(password.data)
        print(tinkamas_slaptazodis)

        if not tinkamas_slaptazodis:
            raise ValidationError("Slaptažodis netinkamas")
