#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2018/12/29  22:36
# @Author: 余浪人
# @email: yulangren520@gmail.com
# @Company:
from apps import create_app

app = create_app('apps.setting.Dev_CMS_Config')


if __name__ == '__main__':
    from apps.models import db
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0")
