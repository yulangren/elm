#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2019/1/3  13:01
# @Author: 余浪人
# @email: yulangren520@gmail.com

""" 验证修改传入参数是否合法 """
from flask import abort
def check_shop(shop):
    if shop is None:
        return abort(404)