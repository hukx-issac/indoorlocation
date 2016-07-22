# coding:utf-8
from indoorlocation import db
from werkzeug.security import generate_password_hash, check_password_hash


# 用户模型
class User(db.Model):
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
    role = db.Column(db.String(10), unique=True, nullable=False)
    users = db.relationship('User', backref='role')

    def __init__(self, id, role = '普通用户'):
        self.id = id
        self.role = role