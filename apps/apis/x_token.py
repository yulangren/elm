#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2019/1/7  17:27
# @Author: 余浪人
# @email: yulangren520@gmail.com

# 获取一个token值
from functools import wraps

from flask import request, jsonify, g
from itsdangerous import SignatureExpired, BadSignature, TimedJSONWebSignatureSerializer


# 验证to_kent
def check_token(old):
    @wraps(old)
    def inner(*args, **kwargs):
        if 'x_access_token' in request.cookies:
            token = request.cookies.get('x_access_token')
        else:
            return jsonify({"status": 0, "message": "token is None"})
        s1 = TimedJSONWebSignatureSerializer(secret_key='abdf12312d')
        try:
            data = s1.loads(token)
        except SignatureExpired:
            return jsonify({"status": 1, "message": "token值过期"})
        except BadSignature:
            return jsonify({"status": 2, "message": "token值无效"})
        xuid = data.get('token')  # 获取值
        g.xuid = xuid
        res = old(*args, **kwargs)
        return res
    return inner
