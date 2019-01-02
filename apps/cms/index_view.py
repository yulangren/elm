#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2018/12/29  22:31
# @Author: 余浪人
# @email: yulangren520@gmail.com
import json
import uuid
from apps.cms import cms_bp
from flask import request, render_template, redirect, url_for, flash
from apps.forms.form import Business_reg, Login_Form
from apps.models import db
from apps.models.merchant_model import Merchant_User_Model, Shop_Model, Dishes_Class_Model, Dishes_Detail_Model
from apps.cms.verify_view import check_password
from apps.forms.shop_form import Shop_Form, Dishes_Class_Form, Dishes_Detail_Form
from flask_login import login_user, login_required, logout_user, current_user


# 商家用户注册
@cms_bp.route('/reg_user/', endpoint='reg_user', methods=['GET', 'POST'])
def reg_user():  # 商家用户注册
    form = Business_reg(request.form)
    if request.method == 'POST' and form.validate():
        merchant = Merchant_User_Model()
        merchant.set_attr(form.data)
        db.session.add(merchant)
        db.session.commit()
        return redirect(url_for(endpoint='.login'))
    return render_template('user_register.html', form=form, page_name='商家注册中心',
                           stat='已有', atonce='马上登录', link=url_for(endpoint='.login'))


# 商家登录
@cms_bp.route('/login_user/', endpoint='login', methods=['POST', 'GET'])
def login():
    form = Login_Form(request.form)
    if request.method == 'POST' and form.validate():
        # 查询数据库 验证用户信息
        user = db.session.query(Merchant_User_Model).filter_by(username=form.username.data).first()  # 只查询一个
        if user is None:
            return redirect(url_for(endpoint='.reg_user'))
        else:
            if check_password(user.password, password=form.password.data):
                print()
                login_user(user)
                return redirect(url_for(endpoint='.end_index'))
            form.password.errors='密码错误!'
    return render_template('user_register.html', form=form, page_name='登录',
                           stat='没有', atonce='马上注册', link=url_for(endpoint='.reg_user'))


# # 商家用户注销登陆
@cms_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for(endpoint='.login'))


# 商家后台首页页面(登录后可见)
@cms_bp.route('/admin/', endpoint='end_index', methods=['GET', 'POST'])
@login_required
def end_index():
    # 当前用户id
    present_id = current_user.id
    # 查询当前用户的店铺
    shops = db.session.query(Shop_Model).filter(Shop_Model.seller_id == present_id).all()
    return render_template('end_index.html', shops=shops)


# 添加店铺(登录后可见)
@cms_bp.route('/add_shop/', endpoint='add_shop', methods=['GET', 'POST'])
@login_required
def add_shop():
    form = Shop_Form(request.form)
    if request.method == "POST":
        merchant = Shop_Model()
        merchant.set_attr(form.data)
        merchant.seller_id = current_user.id  # 当前用户的id
        merchant.pub_id = uuid.uuid4().time_low
        db.session.add(merchant)
        db.session.commit()
        return redirect(url_for(endpoint='.end_index'))
    return render_template('add_shop.html', form=form, page_context='添加')


@cms_bp.route('/update_shop/<int:id>')
@login_required
def update_shop(id):
    # 查询数据准备回显数据
    data = Shop_Model.query.filter_by(id=id, seller_id=current_user.id).first()
    data_s = Shop_Form()
    return render_template('add_shop.html', form=data_s, page_context='更新')


# 添加分类(登录后可见)
@cms_bp.route('/add_cate/', endpoint='add_cate', methods=['GET', 'POST'])
@login_required
def add_cate():
    form = Dishes_Class_Form(request.form)
    if request.method == "POST" and form.validate():
        dishes_class = Dishes_Class_Model()
        dishes_class.set_attr(form.data)
        dishes_class.merchant_id = current_user.id  # 当前商家
        db.session.add(dishes_class)
        db.session.commit()
        return redirect(url_for(endpoint='.end_index'))  # 添加成功,跳转至显示列表页
    result = db.session.query(Shop_Model).filter(Shop_Model.seller_id == current_user.id, ).all()
    form.shop_id.choices += [(r.id, r.shop_name) for r in result]
    return render_template('add_cate.html', form=form, page_context='添加')


# 添加菜品
@cms_bp.route('/add_food/', endpoint='add_food', methods=['GET', 'POST'])
@login_required
def add_food():
    form = Dishes_Detail_Form(request.form)
    if request.method == "POST":
        dishes_detail = Dishes_Detail_Model()
        dishes_detail.set_attr(form.data)
        dishes_detail.shop_id = current_user.id
        return '添加成功'
    result = db.session.query(Dishes_Class_Model).filter(Dishes_Class_Model.merchant_id == current_user.id, )
    form.category_id.choices += [(r.id, r.name) for r in result]
    return render_template('add_food.html', form=form, page_context='添加')
