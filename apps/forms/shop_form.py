#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2019/1/1  0:15
# @Author: 余浪人
# @email: yulangren520@gmail.com


from wtforms import Form, StringField, validators, BooleanField, FloatField, FileField, SelectField

from apps.models.merchant_model import Shop_Model


class Shop_Form(Form):
    shop_name = StringField(label='店铺名称', validators=[
        validators.DataRequired(message='店铺名称不能为空'),
        validators.length(min=2, message='店铺名字过短'),
        validators.length(max=10, message='店铺名字过长'),
    ], render_kw={"placeholder": "请输入店铺名称", "class": "form-control"})
    brand = BooleanField(label='品牌', render_kw={"class": "inlineRadioOptions", "style": "margin-top: 15px;"})
    on_time = BooleanField(label='准时送达', render_kw={"class": "inlineRadioOptions", "style": "margin-top: 15px;"})
    hummingbird = BooleanField(label='蜂鸟配送', render_kw={"class": "inlineRadioOptions", "style": "margin-top: 15px;"})
    protect = BooleanField(label='提供保险', render_kw={"class": "inlineRadioOptions", "style": "margin-top: 15px;"})
    ticket = BooleanField(label='提供发票', render_kw={"class": "inlineRadioOptions", "style": "margin-top: 15px;"})
    standard = BooleanField(label='准标记', render_kw={"class": "inlineRadioOptions", "style": "margin-top: 15px;"})
    start_send = FloatField(label='起送金额', validators=[validators.DataRequired(message='请填写起送金额')],
                            render_kw={"placeholder": "请输入起送价格", "class": "form-control"})
    send_cost = FloatField(label='配送费用', validators=[validators.DataRequired(message='请填写配送费用')],
                           render_kw={"placeholder": "请输入配送费用", "class": "form-control"})
    notice = StringField(label='店铺公告', render_kw={"placeholder": "请输入店铺公告", "class": "form-control"})
    discount = StringField(label='优惠信息', render_kw={"placeholder": "请输入优惠信息", "class": "form-control"})
    shop_img = FileField(label='店铺图片', render_kw={"class": "btn "})

    # def validate_shop_name(self, object):
    #     cou = Shop_Model.query.filter(Shop_Model.shop_name == self.shop_name.data).count()
    #     print(cou)
    #     if cou:
    #         raise validators.ValidationError("店铺名不可重复!")




# 菜品分类模型
class Dishes_Class_Form(Form):
    shop_id = SelectField(label='店铺分类', choices=[('default', '请选择'), ], render_kw={"class": "form-control"})
    name = StringField(label='菜品分类名称', validators=[
        validators.DataRequired(message='请输入菜品分类名'),
        validators.length(min=1, message='菜品分类名长度不符'), ],
                       render_kw={"placeholder": "请输入菜品分类名", "class": "form-control"})
    description = StringField(label='菜品分类描述', render_kw={"placeholder": "请输入菜品分类描述", "class": "form-control"})
    type_accumulation = StringField(label='菜品分类编号', render_kw={"placeholder": "请输入菜品分类编号", "class": "form-control"})
    is_default = BooleanField(label='设为默认')


# 菜品详细模型
class Dishes_Detail_Form(Form):
    goods_name = StringField(label='菜品名称', validators=[
        validators.DataRequired(message='请输入菜品名'), validators.length(min=1, message='菜品名长度不符'),
    ], render_kw={"placeholder": "请输入菜品名", "class": "form-control"})
    category_id = SelectField(label='菜品分类', choices=[('default', '请选择')], render_kw={"class": "form-control"})
    goods_price = FloatField(label='菜品价格', validators=[validators.DataRequired(message='请输入菜品价格')],
                             render_kw={"placeholder": "请输入菜品价格", "class": "form-control"})
    description = StringField(label='菜品描述', render_kw={"placeholder": "请输入菜品描述", "class": "form-control"})
    tips = StringField(label='菜品提示', render_kw={"placeholder": "请输入菜品提示", "class": "form-control"})
    goods_img = FileField(label='菜品图片', render_kw={'class': 'file '})
