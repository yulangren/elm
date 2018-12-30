#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2018/12/29  22:31
# @Author: 余浪人
# @email: yulangren520@gmail.com

from apps.cms import cms_bp
from flask import request, render_template, redirect, url_for
from apps.forms.form import Business_reg, Login_Form
from apps.models import db
from apps.models.merchant_model import MerchantUser


@cms_bp.route('/reg_user/', endpoint='reg_user', methods=['GET', 'POST'])
def reg_user():  # 商家用户注册
    form = Business_reg(request.form)
    if request.method == 'POST' and form.validate():
        merchant = MerchantUser()
        merchant.set_attr(form.data)
        db.session.add(merchant)
        db.session.commit()
        return redirect(url_for(endpoint='.login_user'))
    return render_template('user_register.html', form=form, page_name='商家注册中心',
                           stat='已有', atonce='马上登录', link=url_for(endpoint='.login_user'))


@cms_bp.route('/login_user/', endpoint='login_user', methods=['POST', 'GET'])
def login_user():
    form = Login_Form()
    if request.method == 'POST' and form.validate():
        # 验证用户信息并查询
        return '登录成功跳转'
    return render_template('user_register.html', form=form, page_name='商家登录中心',
                           stat='没有', atonce='马上注册', link=url_for(endpoint='.reg_user'))
