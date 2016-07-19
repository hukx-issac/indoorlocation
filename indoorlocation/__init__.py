# coding:utf-8
from flask import Flask
from flask_bootstrap import Bootstrap
from indoorlocation.views import login

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY']='RRR'
app.register_blueprint(login.main)