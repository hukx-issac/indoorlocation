# coding:utf-8
import os, config
from flask import Blueprint, render_template, flash,redirect, url_for, request, json, Response, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from indoorlocation.models import db, Path, User

main = Blueprint('map_manage', __name__)


# 上传路径
@main.route('/home/mapManage/myPath', methods=['GET', 'POST'])
@login_required
def myPath():
    if request.method == 'POST':
        # 检查post请求是否有文件
        if 'file' not in request.files:
            flash(u'请求没有文件！')
            return redirect(request.url)
        file = request.files['file']
        # 检测用户是否选择了文件
        if file.filename == '':
            flash(u'没有选择文件 ！')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        # 上传文件的目录
        UPLOAD_FOLDER = config.Config.UPLOAD_FOLDER
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        f = open(os.path.join(UPLOAD_FOLDER, filename),'r')
        data = json.load(f)
        try:
            user = User.query.filter_by(username=data['information']['upload_username']).first()
            path = Path(path=str(data['path']), caption=data['information']['user_description'], user_id=user.id)
        except KeyError as e:
            return jsonify({'error': "upload fail. Please check the content of your file "})
        db.session.add(path)
        db.session.commit()
        f.close()
        flash(u'上传成功')
    # 查用户信息
    user = User.query.filter_by(username = current_user.username).first()
    data = {}
    basic_info = {"realname":user.realname, "username":user.username, "role":user.role.role,"num":user.path.count()}
    path = []
    for p in user.path:
        d = {"id":p.id, "caption":p.caption, "user_id":p.user_id}
        path.append(d)
    data['basic_info'] = basic_info
    data['path'] = path
    return render_template('mapManage.html',data=data)

@main.route('/home/mapManage/download', methods=['GET', 'POST'])
@login_required
def download():
    path = Path.query.all()
    data = {}
    data['number'] = len(path)
    content = []
    for p in path:
        temp = {}
        temp['id'] = p.id
        temp['username'] = p.user.username
        temp['caption'] = p.caption
        content.append(temp)
    data['content'] = content
    return json.dumps(data)


@main.route('/home/mapManage/downloadOne', methods=['GET', 'POST'])
@login_required
def downloadOned():
    data = {}
    path = Path.query.filter_by(id=request.form['id']).first()
    if path is not None:
        data['content'] = [{"id":path.id, "username":path.user.username, "caption":path.caption}]
        num = 1
    else:
        data['content'] = []
        num = 0
    data['number'] = num
    return json.dumps(data)


@main.route('/home/mapManage/selectPath', methods=['GET', 'POST'])
@login_required
def selectAllPath():
    return render_template('downloadPath.html')