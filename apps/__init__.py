#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2018/12/29  22:17
# @Author: 余浪人
# @email: yulangren520@gmail.com


from flask import Flask


# 注册login服务
def login_msg(app: Flask):
    app.secret_key = 's3cr3t'
    from apps.libs import login_manager
    login_manager.session_protection = 'strong'  # 当浏览器关闭时 cookie和session将失效
    login_manager.login_view = '/login_user/'
    login_manager.login_message = u"请登陆!"
    login_manager.init_app(app=app)


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
    # 注册用户登陆
    login_msg(app=app)
    return app
