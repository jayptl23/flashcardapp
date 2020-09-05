from flask import Blueprint
from main import bcrypt, db
from flask import render_template, url_for, redirect, flash
from main.users.forms import RegistrationForm, LoginForm
from main.models import User
from flask_login import current_user, login_user, logout_user, login_required

users = Blueprint('users', __name__)


@users.route('/', methods=['GET', 'POST'])
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('decks.all_decks'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Invalid credentials', 'danger')
            return redirect(url_for('users.login'))
        login_user(user)
        return redirect(url_for('decks.all_decks'))
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! You may now login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)
