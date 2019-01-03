#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2019/1/3  19:13
# @Author: 余浪人
# @email: yulangren520@gmail.com
from apps.models.merchant_model import Dishes_Class_Model, Shop_Model


def get_shopUuid(form_data):
    dishes_class_id = Dishes_Class_Model.query.filter_by(id=form_data).first().shop_id  # 店铺id
    shop_pub_id = Shop_Model.query.filter_by(id=dishes_class_id).first().pub_id
    return shop_pub_id