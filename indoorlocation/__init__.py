# coding:utf-8
from flask import Flask
from flask_bootstrap import Bootstrap
from indoorlocation.views import login

# APP_CONFIG_FILE = ''
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
# app.config.from_envvar('APP_CONFIG_FILE')
bootstrap = Bootstrap(app)
app.register_blueprint(login.main)

