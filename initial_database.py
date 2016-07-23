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

    def __init__(self, username, password, role_id=3):
        self.username = username
        self.password = password
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
    users = db.relationship('User', backref='role')

    def __init__(self, id, role = 'generaluser'):
        self.id = id
        self.role = role


db.drop_all()
db.create_all()


# 数据库初始化
# 用户user身份identity
supermanager = Role(1, 'supermanager')
manager = Role(2, 'manager')
generaluser = Role(3, 'generaluser')
db.session.add(manager)
db.session.add(generaluser)
db.session.add(supermanager)
db.session.commit()

# 初始化第一个超级管理员
firstperson= User('qwe', '123',1)
secondperson= User('asd', '123',2)
db.session.add(firstperson)
db.session.add(secondperson)
db.session.commit()