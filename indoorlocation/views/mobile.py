# coding:utf-8
from flask_httpauth import HTTPBasicAuth
from flask import Blueprint, g, jsonify, request, json
from indoorlocation.models import db, Path, User


main = Blueprint('mobile', __name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verfy_password(username_or_token, password):
    if password == '':
        g.current_user = User.verify_auth_token(username_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(username=username_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@main.route('/mobile/token')
@auth.login_required
def get_token():
    if g.token_used:
        return jsonify({'error':'Invalid, you have token already !'})
    return jsonify({'token':g.current_user.generate_auth_token(3600), 'expiration':3600})


@main.route('/mobile/test')
@auth.login_required
def test():
    return "success ！ hkx"


@main.route('/mobile/upload/path',methods=['GET', 'POST'])
def upload():
    try:
        data = request.data
        data = json.loads(data)
        user = User.query.filter_by(username=data['information']['upload_username']).first()
    except KeyError as e:
        return jsonify({'error':"upload fail. We can't find the upload_username or the key 'path' "})
    path = Path(path=data['path'], caption=data['information']['user_description'],user_id = user.id)
    db.session.add(path)
    db.session.commit()
    return jsonify({'status':'upload sucess'})


@main.route('/mobile/download/path',methods=['GET', 'POST'])
def download():
    try:
        path = Path.query.filter_by(id=int(request.form['id'])).first()
    except KeyError as e:
        return jsonify({'error':"download fail. we can't find the key 'id'"})
    if path is not None:
        data = {}
        data['information'] = {'upload_username': path.user.username,'user_description':path.caption,'path_id':path.id}
        data['path'] = path.path
        return jsonify(data)
    else:
        return jsonify({'error':'the id of path is not existed !'})


@main.route('/mobile/searchAllPath',methods=['GET', 'POST'])
def searchAllPath():
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
    return jsonify(data)
