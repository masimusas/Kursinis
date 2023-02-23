from wtforms import SubmitField, DateField, SelectField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm
import app
from wtforms_sqlalchemy.fields import QuerySelectField

def type_query():
    with app.app.app_context():
        return app.TypeVacation.query.all()


class VacationForm(FlaskForm):
    datefrom = DateField('Data nuo')
    dateto = DateField('Data iki')
    type = QuerySelectField(query_factory=type_query, allow_blank=False, get_label="title")
    submit = SubmitField('Pateikti')

