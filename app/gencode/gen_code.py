from . import gencode_blueprint
import qrcode
from io import BytesIO
from flask import request, jsonify, g, url_for, current_app,send_file
import time
import base64
from ..decorators import allow_cross_domain

"""
@api {GET} /api/v1.0/code/route 获得设置wifi网络的二维码
@apiGroup gen_code
@apiName 设置wifi
@apiParam (params) {String} ssid wifi名字 
@apiParam (params) {String} password wifi密码
@apiParam (params) {String} auth_method wifi认证方式 默认WPA2PSK
@apiParam (params) {String} crypto_method wifi加密方式 默认AES

@apiSuccess {Array} operators 返回二维码的base64

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
      status:'success',
      img_base64: '图片的base64'
         
    }
"""

@gencode_blueprint.route('/code/route', methods=['GET','POST'])
@allow_cross_domain
def gen_code_route():
    ssid = request.form.get("ssid")
    password = request.form.get("password")
    auth_method = request.form.get("auth_method", "WPA2PSK")
    crypto_method = request.form.get("crypto_method", "AES")
    print("arg", request.args.items())
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data("SSID:{ssid}\n{auth_method},{crypto_method},{password}\nAA55".format(
        ssid=ssid,
        auth_method=auth_method,
        crypto_method=crypto_method,
        password=password))
    qr.make(fit=True)

    file = BytesIO()
    img = qr.make_image()

    img.save(file)
    file.seek(0)

    img_base64 = base64.b64encode(bytes(file.read()))

    return jsonify(status='success', img_base64=img_base64)

"""
@api {GET} /api/v1.0/code/server 获得设置端口和host的二维码
@apiGroup gen_code
@apiName 设置服务器
@apiSuccess {Array} operators 返回二维码的base64

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
      status:'success',
      img_base64: '图片的base64'
         
    }
"""

@gencode_blueprint.route('/code/server', methods=['GET'])
@allow_cross_domain
def gen_code_server():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data("IP:{port},{host}\nAA55".format(
        port=current_app.custom_net_setting.get('port'),
        host=current_app.custom_net_setting.get('host')
    ))
    qr.make(fit=True)

    file = BytesIO()
    img = qr.make_image()

    img.save(file)
    file.seek(0)

    img_base64 = base64.b64encode(bytes(file.read()))

    return jsonify(status='success', img_base64=img_base64)
"""
@api {GET} /api/v1.0/code/sn 获得设置sn的二维码
@apiGroup gen_code
@apiName 设置sn
@apiParam (params) {String} sn 8位sn码 会自动转换成大写.

@apiSuccess {Array} operators 返回二维码的base64

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
      status:'success',
      img_base64: '图片的base64'
         
    }
"""
@gencode_blueprint.route('/code/sn', methods=['GET'])
@allow_cross_domain
def gen_code_sh():

    sn = request.args.get('sn')

    if sn is None:
        return "sn 不能为空"

    if len(sn) != 8:
        return "sn 长度必须为8"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data("{}".format(sn.upper()))
    qr.make(fit=True)

    file = BytesIO()
    img = qr.make_image()

    img.save(file)
    file.seek(0)

    img_base64 = base64.b64encode(bytes(file.read()))

    return jsonify(status='success', img_base64=img_base64)