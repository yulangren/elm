#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2018/12/29  22:17
# @Author: 余浪人
# @email: yulangren520@gmail.com
# @Company: 

from flask import Flask


# 注册数据库服务
def register_db(app: Flask):
    from apps.models import db
    db.init_app(app=app)


# 注册蓝图
def register_cms_bp(app: Flask):
    from apps.cms import cms_bp
    app.register_blueprint(cms_bp)


# 创建APP
def create_app(config: str):
    app = Flask(__name__)
    # 设置APP的配置文件
    app.config.from_object(config)
    # 注册数据库
    register_db(app=app)
    # 调用注册蓝图
    register_cms_bp(app=app)
    return app
