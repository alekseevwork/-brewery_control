from flask import Blueprint ,flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user

from webapp.user.forms import LoginForm
from webapp.user.models import User
from webapp.tank.models import Measuring

blueprint = Blueprint('user', __name__)
    
@blueprint.route('/login')
def login():
    if current_user.is_authenticated:

        return render_template('base.html', title='authenticated true') # заглушка, пока нет главной страницы

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

            return render_template('base.html', title='Login') # заглушка, пока нет главной страницы
          
    flash('Неправильные имя или пароль')
    return redirect(url_for('user.login'))

@blueprint.route('/logout')
def logout():
    logout_user()

    return render_template('base.html', title='render logout') # заглушка, пока нет главной страницы


@blueprint.route('/')
def home_page():
    content = Measuring.query.all()
    return render_template('home.html', title='Главная страница', context=content)