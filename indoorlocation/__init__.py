# coding:utf-8
from flask import Flask
from indoorlocation.views import login
from config import config
from flask_bootstrap import Bootstrap
from .views.login import login_manager
from models import db

bootstrap = Bootstrap()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
login_manager.login_message = u"请登录您的账户!"


def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])    # 加载根目录配置
    app.config.from_pyfile('development_config.py')    # 从instance文件夹中加载配置

    app.register_blueprint(login.main)  # 注册蓝本
    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    return app