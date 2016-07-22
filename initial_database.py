# coding:utf-8
from indoorlocation import db
from indoorlocation.models import *

db.drop_all()
db.create_all()

# 用户user身份identity
supermanager = Role(1, '超级管理员')
manager = Role(2, '管理员')
generaluser = Role(3, '普通用户')
db.session.add(manager)
db.session.add(generaluser)
db.session.add(supermanager)
db.session.commit()

# 初始化第一个超级管理员
firstperson= User('supermanager', '123456',1)
db.session.add(firstperson)
db.session.commit()