from . import gencode
import qrcode
from io import BytesIO
from flask import request, jsonify, g, url_for, current_app,send_file
import time
from . import gencode

"""
@api {GET} /api/v1.0/code/route 获得设置wifi网络的二维码
@apiGroup gen_code
@apiName 设置server

"""

@gencode.route('/code/route', methods=['GET'])
def gen_code_route():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data("SSID:{ssid}\n{auth_method},{crypto_method},{password}\nAA55".format(
        ssid=current_app.custom_net_setting.get('ssid'),
        auth_method=current_app.custom_net_setting.get('auth_method'),
        crypto_method=current_app.custom_net_setting.get('crypto_method'),
        password=current_app.custom_net_setting.get('password')))
    qr.make(fit=True)

    file = BytesIO()
    img = qr.make_image()

    img.save(file)
    file.seek(0)

    return send_file(file, attachment_filename=str(int(time.time()))+".png", mimetype='image/png')

"""

@api {GET} /api/v1.0/code/server 获得设置端口和host的二维码
@apiGroup gen_code
@apiName 设置网络

"""

@gencode.route('/code/server', methods=['GET'])

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

    return send_file(file, attachment_filename=str(int(time.time()))+".png", mimetype='image/png')

"""

@api {GET} /api/v1.0/code/sn 获得设置sn的二维码
@apiGroup gen_code
@apiName 设置sn
@apiParam (params) {String} sn 8位sn码 会自动转换成大写.

"""
@gencode.route('/code/sn', methods=['GET'])

def gen_code_sh():

    sn = request.args.get('sn')

    if sn is None:
        return "sn can`t be None"

    if len(sn) != 8:
        return "sn must 8 length"

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
    return send_file(file, attachment_filename=str(int(time.time()))+".png", mimetype='image/png')
