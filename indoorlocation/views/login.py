# coding:utf-8
from flask import Flask, Blueprint, render_template

from indoorlocation.forms import *

main = Blueprint('login', __name__)

# 管理员登录接口
@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)