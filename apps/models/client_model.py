#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2019/1/7  14:43
# @Author: 余浪人
# @email: yulangren520@gmail.com
import datetime

from apps.models import db, BaseModel
from apps.models.merchant_model import Shop_Model


# 用户模型


class User(BaseModel):
    name = db.Column(db.String(16), comment='用户名')
    password = db.Column(db.String(128), comment='密码')
    tel = db.Column(db.String(11), comment='电话号码')

    def __repr__(self):
        return self.user


class Address(BaseModel):
    recipients = db.Column(db.String(16), comment='收件人')
    tel = db.Column(db.String(11), comment='收件人电话')
    provence = db.Column(db.String(16), comment='省')
    city = db.Column(db.String(16), comment='市')
    area = db.Column(db.String(16), comment='区')
    detail_address = db.Column(db.String(64), comment='详细地址')
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), comment='所属用户id')
    user = db.relationship('User', backref='address')

    def __repr__(self):
        return self.recipients


class OrderInfo(BaseModel):
    order_code = db.Column(db.String(32), unique=True)
    shop_pid = db.Column(db.String(16), db.ForeignKey(Shop_Model.pub_id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    # 订单送货地址
    order_address = db.Column(db.String(128))
    # 订单价钱
    order_price = db.Column(db.Float, default=0)
    # 订单状态
    order_status = db.Column(db.Integer, default=0)
    # 订单产生时间
    created_time = db.Column(db.DateTime, onupdate=True, default=datetime.datetime.now)
    # 第三方交易号
    trade_sn = db.Column(db.String(128), default='')
    user = db.relationship('User', backref='orderinfo')
    shop = db.relationship('Shop_Model', backref='orderinfo')

    def keys(self):
        return 'order_address', 'order_price', 'order_code'

    def get_status(self):
        if self.order_status == 0:
            return "代付款"
        else:
            return "以付款"


# 订单的商品
class OrderGoods(BaseModel):
    order_id = db.Column(db.Integer, db.ForeignKey(OrderInfo.id))
    # 商品ID号
    goods_id = db.Column(db.Integer)
    # 商品名称
    goods_name = db.Column(db.String(64))
    # 商品图片
    goods_img = db.Column(db.String(128), default='')
    # 商品价钱
    goods_price = db.Column(db.Float)
    # 商品数量
    amount = db.Column(db.Integer)
    order = db.relationship('OrderInfo', backref='ordergoods')

    def keys(self):
        return 'goods_id', 'goods_name', 'goods_price', 'amount', 'goods_img'
