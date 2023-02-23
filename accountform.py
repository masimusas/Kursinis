from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, SelectField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, DataRequired
from flask_wtf import FlaskForm
from app import User, app

class AccountForm(FlaskForm):
    name = StringField("Vardas", [DataRequired()])
    email = EmailField("El.pastas", [DataRequired()])
    submit = SubmitField("Atnaujinti")

    def validate_name(self, name):
        if current_user.name != name.data:  # type: ignore
            with app.app_context():
                this_user = User.query.filter_by(
                    name=name.data).first()
                if this_user:
                    raise ValidationError(
                        "Sis vardas jau yra musu duomenu bazeje")

    def validate_el_pastas(self, email):
        if current_user.email != email.data:  # type: ignore
            with app.app_context():
                this_user = User.query.filter_by(
                    el_pastas=email.data).first()
                if this_user:
                    raise ValidationError(
                        "Sis el pastas jau yra musu duomenu bazeje")
