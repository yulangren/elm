#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2019/1/2  11:40
# @Author: 余浪人
# @email: yulangren520@gmail.com

from flask_login import LoginManager

from apps.models.merchant_model import Merchant_User_Model

login_manager = LoginManager()


@login_manager.user_loader
def load_user(userid: str):
    return Merchant_User_Model.query.get(int(userid))
