# coding:utf-8
from flask_httpauth import HTTPBasicAuth
from flask import Blueprint, g, jsonify
from indoorlocation.models import User

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
        return jsonify({'error':'Invalid'})
    return jsonify({'token':g.current_user.generate_auth_token(3600), 'expiration':3600})


@main.route('/mobile/test')
@auth.login_required
def test():
    return "success ！ hkx"
