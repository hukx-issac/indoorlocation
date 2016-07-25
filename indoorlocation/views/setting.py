# coding:utf-8
from flask import Blueprint, render_template, flash,redirect, url_for, request,session
from flask_login import login_required, current_user
from indoorlocation.forms import ResetPassword
from indoorlocation.models import db

main = Blueprint('setting', __name__)


@main.route('/home/setting', methods=['GET', 'POST'])
@login_required
def setting():
    form = ResetPassword()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            if form.new_password1.data == form.new_password2.data:
                current_user.password = form.new_password1.data
                db.session.add(current_user)
                db.session.commit()
                flash(u'密码修改成功！')
            else:
                flash(u'两次输入的新密码不一致！')
        else:
            flash(u'原始密码错误！')
    return render_template('setting.html', form=form)