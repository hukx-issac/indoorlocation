# coding:utf-8
from flask import Flask, Blueprint, render_template

from indoorlocation.forms import *

main = Blueprint('login', __name__)


# 用户登录接口
@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print form.username.data
        print form.password.data
        print form.select.data
    return render_template('login.html', form=form)
