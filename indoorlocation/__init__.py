# coding:utf-8
from flask import Flask
from flask_bootstrap import Bootstrap
from indoorlocation.views import login

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')    # 加载根目录配置
app.config.from_pyfile('config.py')    # 从instance文件夹中加载配置
bootstrap = Bootstrap(app)
app.register_blueprint(login.main)

