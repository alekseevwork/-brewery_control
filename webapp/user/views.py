from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user

from webapp.user.forms import LoginForm
from webapp.db import db

blueprint = Blueprint('user', __name__, url_prefix='/user')

@blueprint.route('/login')
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('test'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)
    

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('test'))
