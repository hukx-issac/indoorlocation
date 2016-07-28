# coding:utf-8
from flask import Blueprint, render_template, flash,redirect, url_for, request,session
from flask_login import login_required, login_user, LoginManager, logout_user
from indoorlocation.forms import LoginForm
from indoorlocation.models import User
from flask_login import current_user

main = Blueprint('login', __name__)
login_manager = LoginManager()


# 用户登录接口
@main.route('/', methods=['GET', 'POST'], endpoint='login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data) and (user.role.role == form.role.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('login.home'))
        else:
            flash(u'无效的用户名或密码。')
    return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route('/home', endpoint='home')
@login_required
def home():
    return render_template('home.html')


@main.route('/home/logout', endpoint='logout')
@login_required
def logout():
    logout_user()
    flash(u'您已经退出账户！')
    return redirect(url_for('login.home'))


