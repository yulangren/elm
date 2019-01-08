#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2019/1/7  14:50
# @Author: 余浪人
# @email: yulangren520@gmail.com

from wtforms import Form, StringField, validators, PasswordField


# 登录
class User_Form(Form):
    name = StringField('用户名', validators=[
        validators.DataRequired(message='用户名不可为空'),
        validators.length(min=4, max=12, message='长度超出')
    ])
    password = StringField('密码', validators=[
        validators.DataRequired(message='密码不可为空'),
        validators.length(max=32, min=6, message='密码长度不足或超出')
    ])


# 注册
class Register_Form(User_Form):
    password2 = PasswordField(validators=[
        validators.DataRequired(message='密码不能为空!'),
        validators.EqualTo('password', message='两次密码不一致!')
    ], render_kw={"placeholder": "重复密码"})
