#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2018/12/30  11:32
# @Author: 余浪人
# @email: yulangren520@gmail.com
# @Company: 

from apps.models import db, BaseModel


# 商家数据模型
class MerchantUser(BaseModel):
    username = db.Column(db.String(16))  # 用户名
    password = db.Column(db.String(128))  # 商家用户密码

    def __repr__(self):
        return f'商家用户: {self.username}'
