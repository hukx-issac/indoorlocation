# coding:utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Length


# 定义登录表单
class LoginForm(Form):
    username = StringField(u'账号', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField(u'密码', validators=[DataRequired(), Length(1, 20)])
    role = SelectField(u'身份', validators=[DataRequired()], choices=[(u'超级管理员', u'超级管理员'),(u'管理员', u'管理员'), (u'普通用户', u'普通用户')])
    submit = SubmitField(u'登 录')


# 定义管理员账户修改密码表单
class ResetPassword(Form):
    old_password = PasswordField(u'原始密码', validators=[DataRequired(), Length(1,20)])
    new_password1 = PasswordField(u'新密码', validators=[DataRequired(), Length(1,20)])
    new_password2 = PasswordField(u'确认新密码', validators=[DataRequired(), Length(1,20)])
    submit = SubmitField(u'确 认 修 改')


# 超级管理员新增用户表单
class SuperManagerAddUser(Form):
    username = StringField(u'登录账号', validators=[DataRequired(), Length(1,20)])
    password = PasswordField(u'登录密码', validators=[DataRequired(), Length(1,20)])
    realname = StringField(u'用户姓名', validators=[DataRequired(),Length(1,5)])
    role = RadioField(u'角色', choices = [('2', u'管理员'), ('3', u'普通用户')])
    submit = SubmitField(u'提 交')


# 管理员新增用户表单
class ManagerAddUser(Form):
    username = StringField(u'登录账号', validators=[DataRequired(), Length(1,20)])
    password = PasswordField(u'登录密码', validators=[DataRequired(), Length(1,20)])
    realname = StringField(u'用户姓名', validators=[DataRequired(),Length(1,5)])
    role = RadioField(u'角色', choices = [('3', u'普通用户')])
    submit = SubmitField(u'提 交')