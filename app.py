import os
import pythoncom
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import registerform
import loginform
import vacationform
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from docxtpl import DocxTemplate
from datetime import datetime
from flask_mail import Message, Mail
import secret_things
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import passwordresetform
import docx2pdf



basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'Nordan.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_message_category = 'info'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class TypeVacation(db.Model):
    __tablename__ = "typevacation"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    vacations = db.relationship('Vacations', backref='typevacation')


class Vacations(db.Model, UserMixin):
    __tablename__ = "vacations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(60), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    mid = db.Column(db.Integer)
    mname = db.Column(db.String(60), nullable=False)
    msurname = db.Column(db.String(60), nullable=False)
    datefrom = db.Column(db.Date, nullable=False)
    dateto = db.Column(db.Date, nullable=False)
    approved = db.Column(db.Boolean, nullable=True)
    type = db.Column(db.Integer, db.ForeignKey('typevacation.id'))
    creation_date = db.Column(db.DateTime)
    status_date = db.Column(db.DateTime)

class User(db.Model, UserMixin):  # type: ignore
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    surname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), nullable=False, unique=True)
    department = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(254), nullable=False)
    pavaldinys = db.Column(db.Integer, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    vadovas = db.Column(db.Boolean, nullable=False)
    vacations = db.relationship('Vacations', backref='user')


    @staticmethod
    def get_reset_token(user, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': user.id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


def send_reset_email(user):
    token = User.get_reset_token(user)
    msg = Message("Slaptazodzio atnaujinimo uzklausa",
                  sender="spam.marsimus@gmail.com", recipients=[user.email])
    msg.body = f'''Noredami pakeisti slaptazodi paspauskite nuoroda:
    {{{ url_for('reset_token', token=token, _external=True) }}}
    Jei jus nesiuntet prasymo pakeisti slaptazodi, nieko nedarykite'''
    mail.send(msg)

class ManoModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.email == "spam.marsimus@gmail.com"


admin = Admin(app)
admin.add_view(ManoModelView(User, db.session))

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "spam.marsimus@gmail.com"
app.config['MAIL_PASSWORD'] = secret_things.password

mail = Mail(app)

with app.app_context():
    db.create_all()


    @staticmethod
    def get_approve_token(vacations, expires_sec=1209600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'vacations_id': vacations.id}).decode('utf-8')


    @staticmethod
    def verify_approve_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            vacations_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(vacations_id)


def send_vacations_email(vacations):
    token = Vacations.get_approve_token(vacations)
    manager = User.query.filter_by(id=current_user.pavaldinys).first()
    msg = Message("Slaptazodzio atnaujinimo uzklausa",
                  sender="spam.marsimus@gmail.com", recipients=[manager.email])
    msg.body = f'''Noredami pakeisti slaptazodi paspauskite nuoroda:
    {{{ url_for('reset_token', token=token, _external=True) }}}
    Jei jus nesiuntet prasymo pakeisti slaptazodi, nieko nedarykite'''
    mail.send(msg)


@app.route('/vacation_request', methods=['GET', 'POST'])
@login_required
def vacation_request():
    if current_user.is_authenticated:
        form = vacationform.VacationForm()
        manager = User.query.filter_by(id=(current_user.pavaldinys)).first()  
        
        if form.validate_on_submit():
            vacation_type = TypeVacation.query.filter_by(id=(form.type.data.id)).first()
            user_id = current_user.id
            name = current_user.name
            surname = current_user.surname
            mid = manager.id
            mname = manager.name
            msurname = manager.surname
            type = form.type.data.id
            description = vacation_type.description
            datefrom = form.datefrom.data
            dateto = form.dateto.data
            creation_date = datetime.now()
            new_vacation = Vacations(user_id=user_id, name=name, surname=surname, mid=mid, mname=mname, msurname=msurname,
                                     type=type, datefrom=datefrom, dateto=dateto, creation_date=creation_date)
            db.session.add(new_vacation)
            db.session.commit()

            

            doc = DocxTemplate(os.path.join(
            basedir + '/Doc_temp', "temp.docx"))
            date_start = form.datefrom.data
            date_end = form.dateto.data
            date_start_format = form.datefrom.data
            date_end_format = form.dateto.data
            days_sum = date_end_format - date_start_format
            days_format2 = (f'{days_sum.days}')
            context = {'darbuotojas': (name + ' ' + surname),
                       'prasymo_data': creation_date,
                       'atostogu_tipas': description,
                       'atostogu_pradzia': date_start,
                       'atostogu_pabaiga': date_end,
                       'atostogu_trukme': days_format2,
                       'pavaduojantis_darbuotojas': "Martynas Zaksas",
                       'vadovas': (mname + ' ' + msurname)
                       }
            doc.render(context)
            
            doc.save(os.path.join(
                basedir, (f'/GIT/Python_kursas/Modal_05_baigiamasis_patvirtinimas/Doc_output/{new_vacation.id}_{name}{surname}.docx')))

            # send_vacations_email(new_vacation.id)
            

            flash('Sėkmingai užregstravote atostogų prašymą.', 'success')
            return redirect(url_for('my_vacations'))
        return render_template('vacation_request.html', form=form)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = passwordresetform.ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data).first()
        send_reset_email(user)
        flash("Jums issiustas el.laiskas su slaptazodzio keitimo instrukcijomis", 'info')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Uzklausa netinkama arba pasibaigusio galiojimo', 'warning')
        return redirect(url_for('reset_request'))
    form = passwordresetform.PasswordResetForm()
    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  
        user.password = password
        db.session.commit()
        flash("Tavo slaptazodis buvo atnaujintas, gali prisijungti", 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)





@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard')
@login_required
def dashboard():
    try:
        all_vacations = Vacations.query.all()
    except:
        all_vacations = []
    return render_template('dashboard.html', all_vacations=all_vacations)


@app.route("/my_vacations")
@login_required
def my_vacations():
    my_vacations = Vacations.query.filter_by(user_id=current_user.id)
    return render_template("my_vacations.html", my_vacations=my_vacations)


@app.route("/employees_vacations", methods=['GET', 'POST'])
@login_required
def employees_vacations():
    employees_vacations = Vacations.query.filter_by( mid=current_user.id)
    return render_template("employees_vacations.html", employees_vacations=employees_vacations)


@app.route("/patvirtintos_atostogos/<id>", methods=['GET', 'POST'])
@login_required
def confirm_vacation(id):
    vacation = Vacations.query.get(id)
    vacation.approved = 1
    vacation.status_date = datetime.now()
    db.session.commit()


    file_name = (os.path.join(
        basedir, (f'/GIT/Python_kursas/Modal_05_baigiamasis_patvirtinimas/Doc_output/{vacation.id}_{vacation.name}{vacation.surname}')))
    replace_name = file_name.replace("/", "\\")

    # docx file path
    word_file = replace_name+'.docx'
    

    # pdf file path (output)
    pdf_file = replace_name+'.pdf'

    docx2pdf.convert(word_file, pdf_file, pythoncom.CoInitialize())

    employees_vacations = Vacations.query.filter_by(mid=current_user.id)
    return render_template("employees_vacations.html", employees_vacations=employees_vacations)


@app.route("/atmestos_atostogos/<id>", methods=['GET', 'POST'])
@login_required
def reject_vacation(id):
    vacation = Vacations.query.get(id)
    vacation.approved = 0
    vacation.status_date = datetime.now()
    db.session.commit()

    employees_vacations = Vacations.query.filter_by(mid=current_user.id)
    return render_template("employees_vacations.html", employees_vacations=employees_vacations)

@app.route('/top')
def top():
    return render_template('top.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = loginform.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_my.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Prisijungti nepavyko. Patikrinkite el. paštą ir slaptažodį', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    manager = User.query.filter_by(
        id=(current_user.pavaldinys)).first()
    return render_template('account.html', manager=manager)

@ app.route('/register', methods=['GET', 'POST'])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    form = registerform.RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        department = form.department.data
        new_user = User(name=name, surname=surname, email=email, department=department, password=hashed_password, pavaldinys=1, admin=False, vadovas=False)
        db.session.add(new_user)
        db.session.commit()
        flash('Sėkmingai prisiregistravote! Galite prisijungti', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
