#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2019/1/7  10:40
# @Author: 余浪人
# @email: yulangren520@gmail.com

from apps import create_api_app

api_app = create_api_app('apps.setting.Dev_API_Config')


if __name__ == '__main__':
    from apps.models import db
    with api_app.app_context():
        db.create_all()
    api_app.run(port=8080)
