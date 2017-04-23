# coding:utf-8
from flask_httpauth import HTTPBasicAuth
from flask import Blueprint, g, jsonify, request
from indoorlocation.models import db, Path, User


main = Blueprint('mobile', __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
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


@main.route('/mobile/upload/path',methods=['GET', 'POST'])
def upload():
    try:
        data = eval(request.form['path'])
        user = User.query.filter_by(username=data['information']['upload_username']).first()
    except KeyError as e:
        return jsonify({'error':"upload fail. We can't find the upload_username or the key 'path' "})
    path = Path(path=str(data['path']),caption=data['information']['user_description'],user_id = user.id,
                latitude=data['information']['latitude'],longitude=data['information']['longitude'],
                address=data['information']['address'],picture=data['information']['picture'])
    db.session.add(path)
    db.session.commit()
    return jsonify({'status':'upload sucess','path_id':path.id})


@main.route('/mobile/download/path',methods=['GET', 'POST'])
def download():
    try:
        path = Path.query.filter_by(id=int(request.form['id'])).first()
    except KeyError as e:
        return jsonify({'error':"download fail. we can't find the key 'id'"})
    if path is not None:
        data = {}
        data['information'] = {'upload_username': path.user.username,'user_description':path.caption,'path_id':path.id,
                               'latitude':path.latitude,'longitude':path.longitude,'address':path.address,'picture':path.picture}
        data['path'] = eval(path.path)
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
        temp['path_id'] = p.id
        temp['upload_username'] = p.user.username
        temp['user_description'] = p.caption
        temp['latitude'] = p.latitude
        temp['longitude'] = p.longitude
        temp['picture'] = p.picture
        temp['address'] = p.address
        content.append(temp)
    data['content'] = content
    return jsonify(data)


@main.route('/mobile/searchUserPath',methods=['GET', 'POST'])
def searchUserPath():
    try:
        data = request.form['username']
        user = User.query.filter_by(username=data).first()
    except KeyError as e:
        return jsonify({'error':"The username is erorr."})
    paths = user.path
    path_id =[]
    num = 0
    for path in paths:
        num += 1
        path_id.append(path.id)
    result = {'path_id':path_id,'username':data,'number':num}
    return jsonify(result)
