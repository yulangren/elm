#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2019/1/7  10:05
# @Author: 余浪人
# @email: yulangren520@gmail.com
import random
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer
from apps.apis import api_bp
from apps.cms.verify_view import set_password, check_password
from apps.forms.user_check import User_Form
from apps.models.client_model import User, Address
from apps.models.merchant_model import Shop_Model, db, Dishes_Class_Model, Dishes_Detail_Model
from flask import jsonify, request, make_response, current_app
from apps.apis.x_token import check_token


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
            m.set_cookie("uid", str(res.id))
            return m
        return jsonify({"status": 404, "message": "密码或用户名有误!"})
    return jsonify({"status": 404, "message": "不可为空"})


# 获取验证码
@api_bp.route('/sms/', endpoint='get_sms', methods=['GET'])
def get_sms():
    tel = request.args.get('tel')
    if tel:
        yzm = str([random.randint(0, 9) for _ in range(4)]).replace(',', '').replace(' ', '')[1:-1]  # 验证码
        # 设置验证码缓存
        r = current_app.config.get("SESSION_REDIS")
        r.setex(tel, 180, yzm)
        return jsonify({"status": 200, "message": "验证码: %s" % yzm})
    return jsonify({"status": 404, "message": "手机号忘填写"})


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
    r = current_app.config.get("SESSION_REDIS")
    if sms == r.get(tel).decode('utf-8'):
        db.session.add(u1)
        db.session.commit()
        return jsonify({"status": 'true', "message": "注册成功"})
    return jsonify({"status": 404, "message": "验证码错误"})


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
                         detail_address=detail_address, user_id=request.cookies.get('uid'))
            db.session.add(a1)
        db.session.commit()
        return jsonify({"status": 'true', "message": "保存成功!"})
    return jsonify({"status": 404, "message": "添加失败"})


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
        u1 = User.query.filter_by(id=int(request.cookies.get('uid'))).first()
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


# 修改密码
@api_bp.route('/password/', endpoint='update_password', methods=['POST'])
@check_token
def password():
    if request.is_json:
        oldPassword = request.json.get("oldPassword")
        newPassword = request.json.get("newPassword")
    else:
        oldPassword = request.form.get("oldPassword")
        newPassword = request.form.get("newPassword")
    user_id = request.cookies.get('uid')
    if all([oldPassword, newPassword, user_id]):
        u1 = User.query.filter_by(id=int(user_id)).first()
        if check_password(u1.password, oldPassword):
            # 验证成功,修改密码
            u1.password = set_password(newPassword)
            db.session.commit()
            return jsonify({"status": "true", "message": "修改成功"})
        return jsonify({"status": "flase", "message": "修改失败密码错误"})
    return jsonify({"status": "true", "message": "获取用户信息失败,请重新登录"})


# 忘记密码
@api_bp.route('/new_password/', endpoint='new_password', methods=['POST'])
def new_password():
    if request.is_json:
        tel = request.json.get('tel')
        sms = request.json.get('sms')
        password = request.json.get('password')
    else:
        tel = request.form.get('tel')
        sms = request.form.get('sms')
        password = request.form.get('password')
    u1 = User.query.filter_by(tel=tel).first()
    r = current_app.config.get("SESSION_REDIS")
    if all([tel, sms, password]) and u1 and r.get(tel).decode('utf-8') == sms:
        # 验证验证码是否正确
        u1.password = set_password(password)
        db.session.commit()
        return jsonify({"status": "true", "message": "找回密码成功!"})
    return jsonify({"status": "flase", "message": "用户不存在!"})


# 提交订单
@api_bp.route('/cart/', endpoint='add_cart', methods=['POST', 'GET'])
def add_cart():
    user_tel = User.query.filter_by(id=request.cookies.get('uid')).first().tel
    r = current_app.config.get('SESSION_REDIS')
    if request.method == "POST":
        goodslist = request.form.getlist('goodsList[]')
        goodscount = request.form.getlist('goodsCount[]')
        if all([goodslist, goodscount]):
            lists = [(j, x) for j, x in zip(goodslist, goodscount)]
            r.setex('cart_' + user_tel, 60 * 60, str(lists))
            return jsonify({"status": "true", "message": "添加成功"})
        return jsonify({"status": "flase", "message": "添加失败"})
    else:
        cart_data = r.get('cart_' + user_tel).decode('utf-8')
        obj = [(Dishes_Detail_Model.query.filter_by(id=int(j)).first(), int(x)) for j, x in eval(cart_data)]
        data = {
            "goods_list": [{
                "goods_id": x[0].id,
                "goods_name": x[0].goods_name,
                "goods_img": x[0].goods_img,
                "amount": x[1],
                "goods_price": x[0].goods_price
            } for x in obj],
            "totalCost": sum([(x[0].goods_price * x[1]) for x in obj])
        }
    return jsonify(data)


# 添加到订单
@api_bp.route('/order/', endpoint='orders_detail', methods=['GET', 'POST'])
def order():
    if request.method == "POST":
        address_id = request.form.get('address_id')
        data = {"status": "true", "message": "生成订单成功", "order_id": address_id}
    else:
        new_datatime = datetime.datetime.now()  # 获取当前时间
        user_tel = User.query.filter_by(id=request.cookies.get('uid')).first().tel  # 当前用户的手机号
        r = current_app.config.get('SESSION_REDIS')  # 获取redis
        cart_data = r.get('cart_' + user_tel).decode('utf-8')  # Redis购物车数据
        address_id = request.args.get('id')  # 地址ID
        add = Address.query.filter_by(id=int(address_id)).first()  # 地址
        obj = [(Dishes_Detail_Model.query.filter_by(id=int(j)).first(), int(x)) for j, x in eval(cart_data)]
        data = {
            "id": 1,
            "order_code": "0000001",
            "order_birth_time": new_datatime,
            "order_status": "代付款",
            "shop_id": "1",
            "shop_name": "标题",
            "shop_img": "/images/shop-logo.png",
            "goods_list": [{
                "goods_id": x[0].id,
                "goods_name": x[0].goods_name,
                "goods_img": x[0].goods_img,
                "amount": x[1],
                "goods_price": x[0].goods_price
            } for x in obj],
            "order_price": sum([(x[0].goods_price * x[1]) for x in obj]),
            "order_address": add.provence + add.city + add.area + add.detail_address
        }
    return jsonify(data)
