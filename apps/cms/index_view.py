#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2018/12/29  22:31
# @Author: 余浪人
# @email: yulangren520@gmail.com

from apps.cms import cms_bp
from flask import request, render_template, redirect, url_for, flash, jsonify
from apps.forms.form import Business_reg, Login_Form
from apps.libs.checks import check_shop
from apps.libs.get_shop_uuid import get_shopUuid
from apps.models import db
from qiniu import Auth
from apps.models.merchant_model import Merchant_User_Model, Shop_Model, Dishes_Class_Model, Dishes_Detail_Model
from apps.cms.verify_view import check_password
from apps.forms.shop_form import Shop_Form, Dishes_Class_Form, Dishes_Detail_Form
from flask_login import login_user, login_required, logout_user, current_user
from apps.libs.get_uuid import get_uuid
@cms_bp.route('/',endpoint='index',methods=['GET'])
def index():
    return redirect(url_for(endpoint='.end_index'))

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
                login_user(user)
                flash('恭喜你登录成功!正在跳转')
                return redirect(url_for(endpoint='.end_index'))
            else:
                form.password.errors = ('密码错误!',)
    return render_template('user_register.html', form=form, page_name='登录',
                           stat='没有', atonce='马上注册', link=url_for(endpoint='.reg_user'))


# # 商家用户注销登陆
@cms_bp.route('/logout', endpoint='logout')
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
        merchant.pub_id = get_uuid()
        db.session.add(merchant)
        db.session.commit()
        return redirect(url_for(endpoint='.end_index'))
    return render_template('add_shop.html', form=form, page_context='添加')


@cms_bp.route('/update_shop/<update_shop_id>', endpoint='update_shop', methods=['GET', 'POST'])
@login_required
def update_shop(update_shop_id):
    # 查询数据准备
    shop = Shop_Model.query.filter_by(pub_id=update_shop_id, seller_id=current_user.id).first()
    # 验证是否存在,输入是否非法
    check_shop(shop)
    form = Shop_Form(request.form)
    if request.method == "POST" and form.validate():
        shop.set_attr(form.data)
        db.session.commit()
        return redirect(url_for(endpoint='.end_index'))
    else:
        form = Shop_Form(data=dict(shop))  # 回显数据
    return render_template('add_shop.html', form=form, page_context='更新')


# 添加分类(登录后可见)
@cms_bp.route('/add_cate/', endpoint='add_cate', methods=['GET', 'POST'])
@login_required
def add_cate():
    form = Dishes_Class_Form(request.form)
    if request.method == "POST":
        dishes_class = Dishes_Class_Model()
        dishes_class.set_attr(form.data)
        dishes_class.merchant_id = current_user.id  # 当前商家
        dishes_class.category_id = get_uuid()
        db.session.add(dishes_class)
        db.session.commit()
        return redirect(url_for(endpoint='.end_index'))  # 添加成功,跳转至显示列表页
    result = db.session.query(Shop_Model).filter(Shop_Model.seller_id == current_user.id).all()
    form.shop_id.choices += [(r.id, r.shop_name) for r in result]
    return render_template('add_cate.html', form=form, page_context='添加')


@cms_bp.route('/show_cate/<shop_uuid>', endpoint='show_cate')
@login_required
def show_cate(shop_uuid):
    shop_id = Shop_Model.query.filter_by(pub_id=shop_uuid, seller_id=current_user.id).first()  # 获取 店铺
    cate_data = Dishes_Class_Model.query.filter(Dishes_Class_Model.shop_id == shop_id.id).all()  # 获取分类
    su = [([pre.goods_price for pre in cate.dishes_detail_model]) for cate in cate_data]  # 获取当个分类下的价钱
    pre = [sum(i) / len(i) for i in su]  # 以分类进行求和与平均
    for c, p in zip(cate_data, pre):
        c.pre = "%.2f" % p  # 保留两位小数
    return render_template('show_cate.html', cate_data=cate_data, shop_name=shop_id)


@cms_bp.route('/update_cate/<class_uuid>', endpoint='update_cate', methods=['GET', 'POST'])
@login_required
def update_cate(class_uuid):
    # 查询数据准备
    cate = Dishes_Class_Model.query.filter_by(category_id=class_uuid, merchant_id=current_user.id).first()
    # 验证是否存在,输入是否非法
    check_shop(cate)
    form = Dishes_Class_Form(request.form)
    if request.method == "POST":
        cate.set_attr(form.data)
        db.session.commit()
        return redirect(url_for(endpoint='cms_bp.show_cate', shop_uuid=Shop_Model.query.filter_by(
            id=Dishes_Class_Model.query.filter_by(category_id=class_uuid).first().shop_id).first().pub_id))
    else:
        form = Dishes_Class_Form(data=dict(cate))  # 回显数据
        result = db.session.query(Shop_Model).filter(Shop_Model.seller_id == current_user.id)
        form.shop_id.choices += [(r.id, r.shop_name) for r in result]
    return render_template('add_cate.html', form=form)


# 添加菜品
@cms_bp.route('/add_food/', endpoint='add_food', methods=['GET', 'POST'])
@login_required
def add_food():
    form = Dishes_Detail_Form(request.form)
    if request.method == "POST":
        dishes_detail = Dishes_Detail_Model()
        dishes_detail.set_attr(form.data)
        dishes_detail.merchant_id = current_user.id
        dishes_detail.shop_id = get_shopUuid(form.category_id.data)
        db.session.add(dishes_detail)
        db.session.commit()
        return redirect(url_for(endpoint='cms_bp.show_food', shop_uuid=get_shopUuid(form.category_id.data)))
    result = Dishes_Class_Model.query.filter(Dishes_Class_Model.merchant_id == current_user.id).all()
    form.category_id.choices += [(r.id, r.name) for r in result]
    return render_template('add_food.html', form=form, page_context='添加')


@cms_bp.route('/show_food/<shop_uuid>', endpoint='show_food')
@login_required
def show_food(shop_uuid):
    show_detail = Dishes_Detail_Model.query.filter(Dishes_Detail_Model.shop_id == shop_uuid).all()
    shop_name = Shop_Model.query.filter_by(pub_id=shop_uuid).first().shop_name
    return render_template('show_food.html', show_detail=show_detail, shop_name=shop_name)


@cms_bp.route('/update_food/<id>', endpoint='update_food', methods=['GET', 'POST'])
@login_required
def update_food(id):
    # 查询数据准备
    food = Dishes_Detail_Model.query.filter_by(id=id, merchant_id=current_user.id).first()
    # 验证是否存在,输入是否非法
    check_shop(food)
    form = Dishes_Detail_Form(request.form)
    if request.method == "POST":
        food.set_attr(form.data)
        food.shop_id = get_shopUuid(form.category_id.data)
        db.session.commit()
        return redirect(url_for(endpoint='.show_food', shop_uuid=get_shopUuid(form.category_id.data)))
    else:
        form = Dishes_Detail_Form(data=dict(food))  # 回显数据
        result = db.session.query(Dishes_Class_Model).filter(Dishes_Class_Model.merchant_id == current_user.id).all()
        form.category_id.choices += [(r.id, r.name) for r in result]
    return render_template('add_food.html', form=form, page_context='更新')


# 七牛云上传
@cms_bp.route('/uptoken/', methods=['POST', 'GET'])
@login_required
def upload():
    access_key = 'qBqgPsbc1ua-Llrjs1ArsSLGNvQ4adYio8Ja6fXl'
    secret_key = 'UU2lag1W7elV6aAYM4LoBQoky03csPYTBBNQyZ8-'
    q = Auth(access_key=access_key, secret_key=secret_key)
    token = q.upload_token('elm-app')
    return jsonify({"uptoken": token})
