""" Standard routes for Plan'N'Teach """

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
  if request.method=='POST':
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user:
      if check_password_hash(user.password, password):
        flash('Logged in successfully!', category='success')
        login_user(user, remember=True)
        return redirect(url_for('views.homePage'))
      else:
        flash('Incorrect password, try again.', category='error')
    else:
      flash('Unrecognized email, sign up first...', category='error')
      return redirect(url_for('auth.signUp'))
  return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def signUp():
  if request.method == 'POST':
    email = request.form.get('email')
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    password = request.form.get('password')
    password1 = request.form.get('password1')

    user = User.query.filter_by(email=email).first()
    if user:
      flash('Email already exist', category='error')
      return redirect(url_for('auth.login'))
    elif len(email) < 4:
      flash('email format: example@example.com', category='error')
    elif len(firstName) < 2:
      flash('First name must be greater than 2 letters', category='error')
    elif len(lastName) > 20:
      flash('Last name is too long', category='error')
    elif len(password) < 6:
      flash('passwords must be at least 6 characters long', category='error')
    elif password != password1:
      flash('Passwords does not match!', category='error')
    else:
      new_user = User(email=email, firstName=firstName, lastName=lastName,
                      password=generate_password_hash(password, method='pbkdf2:sha256'))
      db.session.add(new_user)
      db.session.commit()
      flash('Account created!', category='success')
      login_user(user, remember=True)
      return redirect(url_for('views.homePage'))

  return render_template("signup.html", user=current_user)
