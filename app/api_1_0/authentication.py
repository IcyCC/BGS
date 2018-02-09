from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth
from ..models import Operator
from . import api

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(operatorname_or_token, password):
    if password == "":
        operator = Operator.verify_auth_token(operatorname_or_token)
        if operator is None:
            return False
        else:
            g.current_user = operator
            return True
    else:
        operator = Operator.query.filter(Operator.tel == operatorname_or_token).first()
        if operator.verify_password(password):
            g.current_user = operator
            return True
        else:
            return False

@api.route('/login')
def operator_login():
    tel = request.json['tel']
    password = request.json['password']
    operator = Operator.query.filter(Operator.tel == tel)
    if operator.verify_password(password):
        return jsonify({
            'status':'success',
            'reason':'the password is true'
        })
    else:
        return jsonify({
            'status':'fail',
            'reason':'the password is wrong'
        })

"""
@api {GET} /api/v1.0/login 通过得到的账号确定密码是否正确(json数据)
@apiGroup authentication
@apiName 通过得到的账号约定密码是否正确

@apiParam (params) {String} tel 操作者的电话号码
@apiParam (params) {String} password 操作者的密码

@apiSuccess {Array} status 返回密码的正确与否

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "status":"success",
        "reason":"the password is true"
    }
    密码错误
    {
        "status":"fail",
        "reason":"the password is wrong"
    }
"""


@api.route('/tokens')
@auth.login_required
def get_auth_token():
    token = g.current_user.generate_auth_token()
    return jsonify({
        'token':token,
        'status':'fail',
        'reason':'the token has been gotten'
    })

"""
@api {GET} /api/v1.0/tokens 根据登陆的账号密码获得token
@apiGroup authentication
@apiName 根据登陆的账号密码获得token

@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} token 返回相应账号的token

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "token":token,
        "status":"success",
        "reason":"the token has been gotten"
    }

"""


