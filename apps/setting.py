#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2018/12/29  22:17
# @Author: 余浪人
# @email: yulangren520@gmail.com
# @Company: 

class Dev_Base_Config():
    # 基础配置清单
    DEBUG = True
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+cymysql://root:248369@localhost:3306/elm"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Dev_CMS_Config(Dev_Base_Config):
    # 开发间段的配置清单
    pass


class Production_CMS_Config(Dev_Base_Config):
    # 开发间段的配置清单
    pass
