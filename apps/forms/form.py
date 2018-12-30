#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2018/12/30  13:30
# @Author: 余浪人
# @email: yulangren520@gmail.com
# @Company:
import serializers as serializers
from wtforms import Form, StringField, PasswordField, validators, ValidationError

from apps.models.merchant_model import MerchantUser


class Login_Form(Form):
    username = StringField(validators=[
        validators.DataRequired(message='手机号/用户名不能为空!'),
        validators.length(min=3, message='用户名长度过短!'),
        validators.length(max=10, message='用户名长度过长!'),
    ],render_kw={ "placeholder": "手机号/用户名"}
                           )
    password = PasswordField(label='密 码:', validators=[
        validators.DataRequired(message='密码不能为空!'),
        validators.length(min=6, message='密码长度不能低于6位!'),
        validators.length(max=32, message='密码长度不能长与32位!'),
    ], render_kw={"placeholder": "密码"}
                             )


class Business_reg(Login_Form):
    password1 = PasswordField(validators=[
        validators.DataRequired(message='密码不能为空!'),
        validators.EqualTo('password', message='两次密码不一致!')
    ], render_kw={"placeholder": "重复密码"}
                              )

    def validate_username(self, _):
        cou = MerchantUser.query.filter(MerchantUser.username == self.username.data).count()
        if cou:
            raise validators.ValidationError("手机号/用户名已存在!")
