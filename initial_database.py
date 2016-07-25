# coding:utf-8
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_login import UserMixin

app = Flask(__name__)
db = SQLAlchemy(app)

# MYSQL-python 做默认的驱动，先安装mysql-python 后再安装sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hkx921023@localhost:3306/indoorlocation'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOEN'] = True    # 自动提交数据库变动
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)


# models 模型
# 用户模型
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    realname = db.Column(db.String(20), nullable=True)
    path = db.relationship('Path', backref='username',lazy='dynamic')     # 定义反向关系

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


# 用户身份模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    role = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship('User', backref='role',lazy='dynamic')     # 定义反向关系

    def __init__(self, id, role = u'普通用户'):
        self.id = id
        self.role = role


# 用户上传的路径模型
class Path(db.Model):
    __tablename__ = 'paths'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    path = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# models 模型 end


db.drop_all()
db.create_all()


# 数据库初始化
# 用户user身份identity
supermanager = Role(1, u'超级管理员')
manager = Role(2, u'管理员')
generaluser = Role(3, u'普通用户')
db.session.add(manager)
db.session.add(generaluser)
db.session.add(supermanager)
db.session.commit()

# 初始化第一个超级管理员
firstperson= User('qwe', '123',1,'supermanager')
secondperson= User('asd', '123',2,'manager')
db.session.add(firstperson)
db.session.add(secondperson)
db.session.commit()