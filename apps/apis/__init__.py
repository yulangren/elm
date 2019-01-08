#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2019/1/7  9:54
# @Author: 余浪人
# @email: yulangren520@gmail.com

from flask import Blueprint

api_bp = Blueprint('api_bp', __name__,url_prefix='/API/v1')

# 导入视图函数
from apps.apis import shop_list
