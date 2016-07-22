# coding:utf-8
from flask import Flask
from indoorlocation.views import login
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config['development'])    # 加载根目录配置
app.config.from_pyfile('development_config.py')    # 从instance文件夹中加载配置
app.register_blueprint(login.main)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


# def create_app(config_name='default'):
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_object(config[config_name])    # 加载根目录配置
#     app.config.from_pyfile('development_config.py')    # 从instance文件夹中加载配置
#
#     bootstrap.init_app(app)
#     db.init_app(app)
#
#     app.register_blueprint(login.main)
#     return app