# import os
# from flask import Flask, render_template, url_for, redirect, flash, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from flask_bcrypt import Bcrypt
# import registerform
# import loginform
# import vacationform
# from flask_admin import Admin  # type: ignore
# from flask_admin.contrib.sqla import ModelView  # type: ignore
# from docxtpl import DocxTemplate
# from datetime import date, datetime
# from flask_mail import Message, Mail
# import secret_things
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # type: ignore
# import passwordresetform
# from app import app, User, Vacations



# @app.route("/approve/<token>", methods=['GET', 'POST'])
# def approve(token):
#     if current_user.is_authenticated:  # type: ignore
#         return redirect(url_for("index"))
#     vacation = Vacations.verify_approve_token(token)
#     if vacation is None:
#         flash('Uzklausa netinkama arba pasibaigusio galiojimo', 'warning')
#         return redirect(url_for('reset_request'))
#     form = passwordresetform.PasswordResetForm()
#     if form.validate_on_submit():
#         password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # type: ignore
#         user.password = password
#         db.session.commit() 
#         flash("Tavo slaptazodis buvo atnaujintas, gali prisijungti", 'success')
#         return redirect(url_for('login'))
#     return render_template('reset_token.html', form=form)
