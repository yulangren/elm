#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2018/12/29  22:17
# @Author: 余浪人
# @email: yulangren520@gmail.com
# @Company:
import datetime


def get_redis():
    from redis import Redis
    r = Redis(host='205.209.163.171', port=6379, db=0, password=None, socket_connect_timeout=10)
    return r


class Dev_Base_Config():
    # 基础配置清单
    DEBUG = True
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+cymysql://root:248369@localhost:3306/elm"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Dev_CMS_Config(Dev_Base_Config):
    # 开发间段的配置清单
    SESSION_TYPE = "redis"
    SESSION_REDIS = get_redis()
    SESSION_USE_SIGNER = True  # 发送到浏览器上session的cookie值进行加密
    SESSION_KEY_PREFIX = "elm"  # 保存到session中的值的前缀
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=30 * 60)  # 设置session过期时间


class Production_CMS_Config(Dev_Base_Config):
    # 开发间段的配置清单
    pass
