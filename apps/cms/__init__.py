#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2018/12/29  22:17
# @Author: 余浪人
# @email: yulangren520@gmail.com
# @Company: 

from flask import Blueprint

# 实例蓝图
cms_bp = Blueprint('cms_bp', __name__)

# 导入index视图
from apps.cms import index_view