from wtforms import StringField, PasswordField, SubmitField, SelectField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_wtf import FlaskForm
from app import User, app

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=3, max=25)], render_kw={"placeholder": "Vardas"})
    surname = StringField(validators=[InputRequired(),Length(min=3, max=25)], render_kw={"placeholder": "Pavardė"})
    email = EmailField(validators=[InputRequired()], render_kw={
                       "placeholder": "Elektroninis paštas"})
    department = SelectField('Skyrius', choices=[(1, "PVC Gamyba"), (2, "ALU Gamyba"), (3, "Administracija")], validators=[InputRequired()], render_kw={"placeholder": "Skyrius"})
    password = PasswordField(validators=[InputRequired(),Length(min=1, max=25)], render_kw={"placeholder": "Slaptažodis"})
    confirm = PasswordField(validators=[EqualTo('password', 'Slaptažodis nesutampa')], render_kw={"placeholder": "Pakartokite slaptažodį"})
    submit = SubmitField('Registruotis')

    def validate_email(self, email):
        with app.app_context():
            print(email.data)
            existing_user_email = User.query.filter_by(email=email.data).first()
            print(existing_user_email)
        if existing_user_email: raise ValidationError('Šis el. pašto adresas panaudotas. Pasirinkite kitą.')
