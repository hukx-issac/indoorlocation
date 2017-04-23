# coding:utf-8
from flask import Blueprint, render_template, flash,redirect, url_for, request, json, Response
from flask_login import login_required, current_user
from ..forms import SuperManagerAddUser, ManagerAddUser
from ..models import User, Role, Path
from indoorlocation.models import db

main = Blueprint('user_manage', __name__)


# 查询普通用户
@main.route('/home/selectUser/generalUser', methods=['GET', 'POST'])
@login_required
def selectGeneralUser():
    return render_template('selectGeneralUser.html')


# 查询管理员
@main.route('/home/selectUser/Manager', methods=['GET', 'POST'])
@login_required
def selectManager():
    return render_template('selectManager.html')

'''
查看用户信息
Json格式
basic_info 用户基本信息, realname 真实姓名, username 用户名, role 用户身份, num 用户上传的路径总数
path 用户上传的路径列表, id 路径编号, caption 路径说明, user_id 路径上传者编号,
{"basic_info":{"realname":user.realname, "username":user.username, "role":user.role.role,,"num":user.path.count()},
"path":[{"id":p.id, "caption":p.caption, "user_id":p.user_id},{...},{...}]
}
'''
@main.route('/home/selectInfo/<path:username>', methods=['GET', 'POST'])
@login_required
def userInfo(username):
    username = username.split('/')[1]
    user = User.query.filter_by(username = username).first()
    data = {}
    basic_info = {"realname":user.realname, "username":user.username, "role":user.role.role,"num":user.path.count()}
    path = []
    for p in user.path:
        d = {"id":p.id, "caption":p.caption, "user_id":p.user_id}
        path.append(d)
    data['basic_info'] = basic_info
    data['path'] = path
    return render_template('userInformation.html',data=data)


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


'''
查询用户API
JSON格式{realname真实姓名 username用户名}，length用户数量:

{"users":[{"realname":user.realname,"username":user.username},{},{}],
"information": {"length":num }
}
'''
# 请求所有普通用户数据
@main.route('/home/selectUser/searchAllGeneral', methods=['GET','POST'])
@login_required
def searchAllGeneral():
    role = Role.query.filter_by(role=u"普通用户").first()
    num = 0
    data = {}
    data1 = []
    for user in role.users:
        num = num + 1
        data1.insert(0,{"realname":user.realname,"username":user.username})
    data["users"] = data1
    data["information"] = {"length":num }
    return json.dumps(data)


# 请求所有管理员数据
@main.route('/home/selectUser/searchAllManager', methods=['GET','POST'])
@login_required
def searchAllManager():
    role = Role.query.filter_by(role=u"管理员").first()
    num = 0
    data = {}
    data1 = []
    for user in role.users:
        num = num + 1
        data1.insert(0,{"realname":user.realname,"username":user.username})
    data["users"] = data1
    data["information"] = {"length":num }
    return json.dumps(data)


# 查找单个用户
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
并返回一个删除的Json格式的状态
'''
@main.route('/remove/user', methods=['POST'])
@login_required
def remove_user():
    user = User.query.filter_by(username=request.form['username']).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        data = {"status": "success"}
    else:
        data = {"status": "fail"}
    return json.dumps(data)


'''
删除路径数据
并返回一个删除的Json格式的状态
'''
@main.route('/remove/path', methods=['POST'])
@login_required
def remove_path():
    path = Path.query.filter_by(id=request.form['path_id']).first()
    if path is not None:
        db.session.delete(path)
        db.session.commit()
        data = {"status": "success"}
    else:
        data = {"status": "fail"}
    return json.dumps(data)


'''
请求下载路径数据
'''
@main.route('/download/path/<int:path_id>',  methods=['POST','GET'])
@login_required
def download_path(path_id):
    path = Path.query.filter_by(id=path_id).first()
    data = {}
    data['information'] = {'upload_username': path.user.username, 'user_description': path.caption, 'path_id': path.id,
                           'latitude': path.latitude, 'longitude': path.longitude, 'address': path.address,'picture': path.picture}
    data['path'] = eval(path.path)
    content = json.dumps(data)
    filename = 'path_'+str(path_id)+'.json'
    return Response(content,
            mimetype='application/json',
            headers={'Content-Disposition':'attachment;filename='+filename})


'''
查看路径数据
'''
@main.route('/view/path/<int:path_id>', methods=['POST','GET'])
@login_required
def view_path(path_id):
    return render_template('viewPath.html')


@main.route('/getpath/<int:path_id>',  methods=['POST','GET'])
@login_required
def get_path(path_id):
    path = Path.query.filter_by(id=path_id).first()
    data = eval(path.path)
    return json.dumps(data)