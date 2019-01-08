#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2019/1/7  10:05
# @Author: 余浪人
# @email: yulangren520@gmail.com
import random

from itsdangerous import TimedJSONWebSignatureSerializer

from apps.cms.verify_view import redis
from apps.apis import api_bp
from apps.cms.verify_view import set_password, check_password
from apps.forms.user_check import User_Form
from apps.models.client_model import User, Address
from apps.models.merchant_model import Shop_Model, db, Dishes_Class_Model
from flask import jsonify, request, make_response
from apps.apis.x_token import check_token

r = redis()


# 首页店铺列表
@api_bp.route('/shop_list/', endpoint='shop_list', methods=['GET'])
def get_shop_list():
    res = Shop_Model.query.all()
    data = [
        {
            "id": x.pub_id,
            "shop_name": x.shop_name,
            "shop_img": x.shop_img,
            "shop_rating": x.shop_rating,
            "brand": x.brand,
            "on_time": x.on_time,
            "fengniao": x.hummingbird,
            "bao": x.protect,
            "piao": x.ticket,
            "zhun": x.standard,
            "start_send": x.start_send,
            "send_cost": x.send_cost,
            "distance": 347,
            "estimate_time": 30,
            "notice": x.notice,
            "discount": x.discount
        }
        for x in res]
    return jsonify(data)


# 获取指定商家接口
@api_bp.route('/shop/', endpoint='shop', methods=['GET'])  # 接收一个UUID
def get_shop():
    shop = Shop_Model.query.filter_by(pub_id=request.args.get('id')).first()
    deshes = Dishes_Class_Model.query.filter(Dishes_Class_Model.shop_id == shop.id)
    data = {
        "id": shop.pub_id,
        "shop_name": shop.shop_name,
        "shop_img": shop.shop_img,
        "shop_rating": shop.shop_rating,
        "brand": shop.brand,
        "on_time": shop.on_time,
        "fengniao": shop.hummingbird,
        "bao": shop.protect,
        "piao": shop.ticket,
        "zhun": shop.standard,
        "start_send": shop.start_send,
        "send_cost": shop.send_cost,
        "distance": 347,
        "estimate_time": 30,
        "notice": shop.notice,
        "discount": shop.discount,
        "evaluate": [
            {
                "user_id": 12344,
                "username": "w******k",
                "user_img": shop.shop_img,
                "time": "2017-2-22",
                "evaluate_code": 5,
                "send_time": 30,
                "evaluate_details": "很好吃"
            }
        ],
        "commodity": [{"description": good_list.type_accumulation,
                       "is_selected": good_list.is_default,
                       "name": good_list.name,
                       "type_accumulation": good_list.type_accumulation,
                       "goods_list": [{
                           "goods_id": goods.id,
                           "goods_name": goods.goods_name,
                           "rating": goods.rating,
                           "goods_price": goods.goods_price,
                           "description": goods.description,
                           "month_sales": goods.month_sales,
                           "rating_count": goods.rating_count,
                           "tips": goods.tips,
                           "satisfy_count": goods.satisfy_count,
                           "satisfy_rate": goods.satisfy_rate,
                           "goods_img": goods.goods_img
                       } for goods in good_list.dishes_detail_model]} for good_list in deshes]
    }
    return jsonify(data)


# 登陆
@api_bp.route('/login/', endpoint='login', methods=['POST'])
def login():
    if request.is_json:
        form = User_Form(request.json)
        name = request.json.get('name')
        password = request.json.get('password')
    else:
        form = User_Form(request.form)
        name = request.form.get('name')
        password = request.form.get('password')
    if all([name, password]):
        res = User.query.filter_by(name=name).first()
        if not res is None and check_password(res.password, password):
            s1 = TimedJSONWebSignatureSerializer(secret_key='abdf12312d', expires_in=60 * 60)  # 过期时间为60秒
            data = s1.dumps({'token': res.id})
            m = make_response(jsonify({"status": 'true', "message": "登录成功", "username": name, "user_id": res.id}))
            m.set_cookie("x_access_token", data)
            return m
        return jsonify({"status": 1, "message": "密码或用户名有误!"})
    return jsonify({"status": 400, "message": "不可为空"})


# 获取验证码
@api_bp.route('/sms/', endpoint='get_sms', methods=['GET'])
def get_sms():
    tel = request.args.get('tel')
    if tel:
        yzm = str([random.randint(0, 9) for _ in range(4)]).replace(',', '').replace(' ', '')[1:-1]  # 验证码
        # 设置验证码缓存
        r.set(tel, yzm)
        r.expire(tel, 180)
        r.save()
        return jsonify({"status": 0, "message": yzm})
    return jsonify({"status": 400, "message": "手机号忘填写"})


# 注册用户
@api_bp.route('/register/', endpoint='register', methods=['POST'])
def register():
    if request.is_json:
        username = request.json.get('username')
        tel = request.json.get('tel')
        sms = request.json.get('sms')
        password = request.json.get('password')
    else:
        username = request.form.get('username')
        tel = request.form.get('tel')
        sms = request.form.get('sms')
        password = request.form.get('password')
    u1 = User(name=username, password=set_password(password), tel=tel)
    if sms == r.get(tel).decode('utf-8'):
        db.session.add(u1)
        db.session.commit()
        return jsonify({"status": 0, "message": "注册成功"})
    return jsonify({"status": 1, "message": "验证码错误"})


# 添加收货地址    更新收货地址
@api_bp.route('/address/', endpoint='add_address', methods=['POST'])
@check_token
def add_address():
    if request.is_json:
        usernmae = request.json.get("name")  # 收件人
        id = request.json.get("id")  # id
        tel = request.json.get("tel")  # 电话
        provence = request.json.get("provence")  # 省
        city = request.json.get("city")  # 市
        area = request.json.get("area")  # 区
        detail_address = request.json.get("detail_address")  # 详细地址
    else:
        usernmae = request.form.get("name")  # 收件人
        id = request.form.get("id")  # id
        tel = request.form.get("tel")  # 电话
        provence = request.form.get("provence")  # 省
        city = request.form.get("city")  # 市
        area = request.form.get("area")  # 区
        detail_address = request.form.get("detail_address")  # 详细地址
    # 判断是否填写数据
    if all([usernmae, tel, provence, city, area, detail_address]):
        if id:
            a1 = Address.query.filter_by(id=id).first()
            a1.recipients = usernmae
            a1.tel = tel
            a1.provence = provence
            a1.city = city
            a1.area = area
            a1.detail_address = detail_address
        else:
            a1 = Address(recipients=usernmae, tel=tel, provence=provence, city=city, area=area,
                         detail_address=detail_address)
            db.session.add(a1)
        db.session.commit()
        return jsonify({"status": 200, "message": "保存成功!"})
    return jsonify({"status": 400, "message": "添加失败"})


# 查看收货地址  更新回显
@api_bp.route('/address/', endpoint='show_address', methods=['GET'])
@check_token
def show_address():
    ida = request.args.get('id')
    if ida:
        Add = Address.query.filter_by(id=ida).first()
        data = {"id": Add.id,
                "provence": Add.provence,
                "city": Add.city,
                "area": Add.area,
                "detail_address": Add.detail_address,
                "name": Add.recipients,
                "tel": Add.tel}
        return jsonify(data)
    else:
        u1 = User.query.filter_by(id=1).first()  # TODO  获取当前用户id
        data = [{
            "id": x.id,
            "provence": x.provence,
            "city": x.city,
            "area": x.area,
            "detail_address": x.detail_address,
            "name": x.recipients,
            "tel": x.tel
        } for x in u1.address]
        return jsonify(data)

