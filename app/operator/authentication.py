from flask import g, jsonify, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_login import login_user
from app.models import Operator

from app.operator import operator_blueprint
from sqlalchemy.exc import OperationalError
from flask_login import current_user, login_required, logout_user

from app import mail, db
import jwt
import datetime
# auth = HTTPBasicAuth()

SECRECT_KEY = 'secret'

def jwtEncoding(some, aud='webkit'):
    encoded2 = jwt.encode(some, SECRECT_KEY, algorithm='HS256')
    return encoded2

def jwtDecoding(token, aud='webkit'):
    print(token.encode())
    decoded = jwt.decode(token, SECRECT_KEY, algorithms=['HS256'])
    return decoded


# @auth.verify_password
# def verify_password(operatorname_or_token, password):
#     if password == "":
#         operator = Operator.verify_auth_token(operatorname_or_token)
#         if operator is None:
#             return False
#         else:
#             g.current_user = operator
#             return True
#     else:
#         operator = Operator.query.filter(Operator.tel == operatorname_or_token).first()
#         if operator.verify_password(password):
#             g.current_user = operator
#             return True
#         else:
#             return False
# """
# 用于判断密码是否正确
# """

# @operator_blueprint.route('/tokens')
# @auth.login_required
# def get_auth_token():
#     token = g.current_user.generate_auth_token()
#     return jsonify({
#         'token':token,
#         'status':'fail',
#         'reason':'the token has been gotten'
#     })
#
# """


@operator_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    operator = Operator.query.filter(Operator.operator_name==username).first()

    if operator is None or not operator.verify_password(password=password):
        return jsonify(status="fail", reason="no this user or password error", data=[])

    userInfo = {
        "id": operator.id,
        "username": operator.operator_name
    }

    token = jwtEncoding(userInfo)
    login_user(operator, remember=True)

    return jsonify(status="success", reason="", operators=[operator.to_json()], token = token.decode())

"""
@api {POST} /login 登录账号(json数据)
@apiGroup authentication
@apiName 登录账号
@apiParam (params) {String} username 登录账号
@apiParam (params) {String} password 新的密码

@apiSuccess {Array} status 登陆情况
@apiSuccess {Array} operator 操作人员信息

@apiSuccessExample Success-Response:
    登陆成功
    {
        "operators":[{
            "url":"医生地址",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名"
        }],
        "status":"success",
        "reason":'',
        "token":"token"
    }
    更改失败
    {
        "status":"fail",
        "reason":"",
        "operators":[]
    }
"""


@operator_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    if request.method == "GET":
        logout_user()
        return jsonify(status="success", reason="", operators=[])

"""
@api {GET} /logout 登出账号(json数据)
@apiGroup operator
@apiName 新建操作者信息

@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} status 登出情况

@apiSuccessExample Success-Response:
    登出成功
    {
        "status":"success",
        "reason":'',
        "operators":[]
    }
"""

@operator_blueprint.route('/change_password', methods = ['PUT'])
def change_password():
    hospital = request.json['hospital']
    office = request.json['office']
    password = request.json['password']
    operator = Operator.query.first()
    if hospital != operator.hospital:
        return jsonify({
            'status':'fail',
            'reason':'the hospital is wrong'
        })
    if office != operator.office:
        return jsonify({
            'status': 'fail',
            'reason': 'the office is wrong'
        })
    operator.password = password
    try:
        db.session.add(operator)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'season': e,
            'operators': []
        })
    return jsonify({
        'status':'success',
        'reason':'',
        'operators':[operator.to_json()]
    })

"""
@api {POST} /operators 修改密码(json数据)
@apiGroup operator
@apiName 修改密码
@apiParam (params) {String} hospital 医院名称
@apiParam (params) {String} office 科室
@apiParam (params) {String} password 新的密码

@apiSuccess {Array} operators 更改后的操作者信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "operators":[{
            "url":"医生地址",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名"
        }],
        "status":"success",
        "reason":''
    }
    更改失败
    {
        "status":"fail",
        "reason":"",
        "operators":[]
    }
"""
