# coding:utf-8
import os, config
from flask import Blueprint, render_template, flash,redirect, url_for, request, json, Response
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from indoorlocation.models import db, Path, User
from user_manage import userInfo

main = Blueprint('map_manage', __name__)


# 上传路径
@main.route('/home/mapManage/upload', methods=['GET', 'POST'])
@login_required
def upload():
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
        path = Path(path=data['path'], caption=data['caption'],user_id = data['user_id'])
        db.session.add(path)
        db.session.commit()
        f.close()
        flash(u'上传成功')

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