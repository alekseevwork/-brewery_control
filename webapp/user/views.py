from flask import Blueprint ,flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user

from webapp.user.forms import LoginForm
from webapp.user.models import User
from webapp.tank.models import Measuring, Tank

blueprint = Blueprint('user', __name__)
    
@blueprint.route('/login')
def login():
    if current_user.is_authenticated:

        return redirect(url_for('user.home_page')) 

    page_title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', title=page_title, form=login_form)

@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли на сайт')

            return redirect(url_for('user.home_page'))
          
    flash('Неправильные имя или пароль')
    return redirect(url_for('user.login'))

@blueprint.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('user.home_page'))


@blueprint.route('/')
def home_page():
    measuring = Measuring.query.order_by(Measuring.create_at.desc()).all()
    all_tanks = Tank.query.order_by(Tank.number).all()
    return render_template('user/home.html', title='Последние измерения', 
    content=[measuring, all_tanks])