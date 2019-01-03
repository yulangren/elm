#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2018/12/30  11:32
# @Author: 余浪人
# @email: yulangren520@gmail.com
# @Company:


from apps.models import db, BaseModel
from flask_login import UserMixin


# 商家数据模型
class Merchant_User_Model(BaseModel, UserMixin):
    username = db.Column(db.String(length=16), comment='用户名')  # 用户名
    password = db.Column(db.String(length=128), comment='用户密码')  # 商家用户密码

    def __repr__(self):
        return f'商家用户: {self.username}'
    # def get_id(self):
    #     return self.username        # 设置用户名


# 店铺模型
class Shop_Model(BaseModel):
    seller_id = db.Column(db.INT, comment='店铺所属商家ID号')
    shop_name = db.Column(db.String(length=32), comment='店铺名称')
    shop_img = db.Column(db.String(length=128), comment='店铺图片')
    shop_rating = db.Column(db.Float, default=5.0, comment='评分')
    brand = db.Column(db.Boolean, default=False, comment='是否是品牌')
    on_time = db.Column(db.Boolean, default=False, comment='是否准时送达')
    hummingbird = db.Column(db.Boolean, default=False, comment='是否蜂鸟配送')
    protect = db.Column(db.Boolean, default=False, comment='是否保标记')
    ticket = db.Column(db.Boolean, default=False, comment='是否票标记')
    standard = db.Column(db.Boolean, default=False, comment='是否准标记')
    start_send = db.Column(db.Float, default=0.00, comment='起送金额')
    send_cost = db.Column(db.Float, default=0.00, comment='配送费')
    notice = db.Column(db.String(length=128), comment='店公告')
    discount = db.Column(db.String(length=512), comment='优惠信息')
    pub_id = db.Column(db.String(16), comment='店铺对外ID号')

    def __repr__(self):
        return f'店铺名称: {self.shop_name}'

    def keys(self):
        return 'shop_name', 'shop_img', 'brand', 'on_time', 'hummingbird', 'protect', 'ticket', 'standard', 'start_send', 'send_cost', 'notice', 'discount'


# 菜品分类模型
class Dishes_Class_Model(BaseModel):
    name = db.Column(db.String(length=16), comment='名称')
    type_accumulation = db.Column(db.String(length=50), comment='菜品编号')
    merchant_id = db.Column(db.INT, comment='所属商家ID')
    shop_id = db.Column(db.INT, comment='所属店铺ID')
    description = db.Column(db.String(length=250), comment='描述')
    is_default = db.Column(db.Boolean, default=False, comment='是否是默认分类')
    category_id = db.Column(db.String(16), comment='分类UUID')

    def __repr__(self):
        return f'菜品分类: {self.name}'

    def keys(self):
        return 'name', 'type_accumulation', 'shop_id', 'description', 'is_default'


# 菜品详细模型
class Dishes_Detail_Model(BaseModel):
    goods_name = db.Column(db.String(length=16), comment='名称')
    merchant_id = db.Column(db.INT, comment='所属商家ID')
    rating = db.Column(db.Float, default=5.0, comment='评分')
    shop_id = db.Column(db.String(16), comment='所属店铺ID')
    category_id = db.Column(db.String(16), comment='所属分类ID')
    goods_price = db.Column(db.Float, comment='价格')
    description = db.Column(db.String(length=250), comment='描述')
    month_sales = db.Column(db.Integer, default=0, comment='月销量')
    rating_count = db.Column(db.Integer, default=0, comment='评分数量')
    tips = db.Column(db.String(length=250), comment='提示信息')
    satisfy_count = db.Column(db.Integer, comment='满意度数量')
    satisfy_rate = db.Column(db.Float, default=5.0, comment='满意度评分')
    goods_img = db.Column(db.String(length=250), comment='商品图片')

    def __repr__(self):
        return f'菜品详细: {self.goods_name}'

    def keys(self):
        return 'goods_name', 'merchant_id', 'shop_id', 'goods_price', 'tips', 'description', 'goods_img', 'category_id'
