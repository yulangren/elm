#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2018/12/29  22:46
# @Author: 余浪人
# @email: yulangren520@gmail.com
# @Company: 

from flask_sqlalchemy import SQLAlchemy
import datetime

# 实例db
db = SQLAlchemy()


# 定义基础数据模型
class BaseModel(db.Model):
    __abstract__ = True  # 设置为基础模型, 不会创建数据表
    id = db.Column(db.Integer, primary_key=True, comment='ID')
    permission = db.Column(db.Integer, default=111, comment='权限,默认读|写|执行')
    create_time = db.Column(db.DATETIME, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DATETIME, default=datetime.datetime.now, comment='更新时间')
    status = db.Column(db.Integer, default=1, comment='状态 -1:禁用  0:删除  1:上架/正常 2:下架')  # 状态

    def set_attr(self, form_data):  # 添加数据 / 只能在表单name与字段名相同时可以使用该方法
        from apps.cms.verify_view import set_password
        for k, v in form_data.items():
            if hasattr(self, k) and k != 'id':
                if k != 'password':
                    setattr(self, k, v)
                else:  # 对密码进行加密
                    setattr(self, k, set_password(v))

    # 强转字典
    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)

# 导入自定义数据模型
from apps.models import merchant_model,client_model


