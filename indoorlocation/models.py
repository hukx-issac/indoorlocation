# coding:utf-8
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

db = SQLAlchemy()


# 用户模型
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    realname = db.Column(db.String(20), nullable=True)
    path = db.relationship('Path', backref='user',lazy='dynamic')     # 定义反向关系

    def __init__(self, username, password, role_id=3, realname = ''):
        self.username = username
        self.password = password
        self.realname = realname
        self.role_id = role_id

    @property
    def password(self):
        raise ArithmeticError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def reset_password(self, newpassword):
        self.password_hash = generate_password_hash(newpassword)

    def generate_auth_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id':self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

# 用户身份模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    role = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy='dynamic')     # 定义反向关系

    def __init__(self, id, role = u'普通用户'):
        self.id = id
        self.role = role


# 用户上传的路径模型
class Path(db.Model):
    __tablename__ = 'paths'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    path = db.Column(db.Text)
    caption = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    
