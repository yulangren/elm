#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2019/1/7  14:43
# @Author: 余浪人
# @email: yulangren520@gmail.com

from apps.models import db, BaseModel



# 用户模型
class User(BaseModel):
    name = db.Column(db.String(16), comment='用户名')
    password = db.Column(db.String(128), comment='密码')
    tel = db.Column(db.String(11), comment='电话号码')

    def __repr__(self):
        return self.user


class Address(BaseModel):
    recipients = db.Column(db.String(16), comment='收件人')
    tel = db.Column(db.String(11),comment='收件人电话')
    provence = db.Column(db.String(16), comment='省')
    city = db.Column(db.String(16), comment='市')
    area = db.Column(db.String(16), comment='区')
    detail_address = db.Column(db.String(64), comment='详细地址')
    user_id = db.Column(db.Integer,db.ForeignKey(User.id),comment='所属用户id')
    user = db.relationship('User', backref='address')

    def __repr__(self):
        return self.recipients