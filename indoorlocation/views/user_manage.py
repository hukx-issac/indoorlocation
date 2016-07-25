# coding:utf-8
from flask import Blueprint, render_template, flash,redirect, url_for, request, json
from flask_login import login_required, current_user
from ..forms import SuperManagerAddUser, ManagerAddUser
from ..models import User
from indoorlocation.forms import ResetPassword
from indoorlocation.models import db

main = Blueprint('user_manage', __name__)


# 新增用户
@main.route('/home/addUser', methods=['GET', 'POST'], endpoint='addUser' )
@login_required
def addUser():
    if current_user.role.role == u"超级管理员":
        form = SuperManagerAddUser()
    elif current_user.role.role == u"管理员":
        form = ManagerAddUser()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash(u'该用户名已存在!')
            return redirect(request.args.get('next') or url_for('user_manage.addUser'))
        else:
            user = User(form.username.data, form.password.data, form.role.data, form.realname.data)
            db.session.add(user)
            db.session.commit()
            flash(u'新增用户成功！')
            return redirect(request.args.get('next') or url_for('user_manage.addUser'))
    return render_template('addUser.html', form=form)


@main.route('/home/selectUser', methods=['GET', 'POST'])
@login_required
def selectUser():
    return render_template('selectUser.html')


'''
查询用户API
JSON格式{realname真实姓名 username用户名}，length用户数量:

{"users":[{"realname":user.realname,"username":user.username},{},{}],
"information": {"length":num }
}
'''
@main.route('/home/selectUser/searchAll', methods=['GET','POST'])
@login_required
def searchAll():
    num = User.query.count()
    users = User.query.all()
    data = {}
    data1 = []
    for user in users:
        data1.insert(0,{"realname":user.realname,"username":user.username})
    data["users"] = data1
    data["information"] = {"length":num }
    return json.dumps(data)


@main.route('/home/selectUser/search', methods=[ 'POST'])
@login_required
def search():
    data = {}
    user = User.query.filter_by(username=request.form['input']).first()
    if user is not None:
        data["users"] = [{"realname":user.realname,"username":user.username}]
        num = 1
    else:
        data["users"] = []
        num = 0
    data["information"] = {"length":num }
    return json.dumps(data)


'''
删除用户数据
并返回一个删除的状态
'''
@main.route('/home/selectUser/remove', methods=['POST'])
@login_required
def remove():
    user = User.query.filter_by(username=request.form['username']).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        data = {"status": "success"}
    else:
        data = {"status": "fail"}
    return json.dumps(data)
