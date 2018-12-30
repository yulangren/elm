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
    id = db.Column(db.Integer, primary_key=True)  # id
    create_time = db.Column(db.DATETIME,default=datetime.datetime.now)  # 创建时间
    status = db.Column(db.Integer, default=1)  # 状态

    def set_attr(self, form_data):  # 添加数据 / 只能在表单name与字段名相同时可以使用该方法
        for k, v in form_data.items():
            if hasattr(self, k) and k != 'id':
                setattr(self, k, v)


# 导入自定义数据模型
from apps.models import merchant_model
