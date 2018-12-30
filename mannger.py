#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2018/12/29  22:17
# @Author: 余浪人
# @email: yulangren520@gmail.com
# @Company:

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps.models import db
from apps import create_app

cms_app = create_app('apps.setting.Dev_CMS_Config')
# 绑定APP调试
manager = Manager(app=cms_app)
# 绑定数据迁移
migrate = Migrate(app=cms_app, db=db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
