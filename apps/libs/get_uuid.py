#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2019/1/3  12:58
# @Author: 余浪人
# @email: yulangren520@gmail.com


import uuid


def get_uuid():
    data = str(uuid.uuid4())
    return ''.join(data.split('-')[:3])
