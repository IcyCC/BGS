from flask import g, jsonify, request, url_for, abort
from flask_httpauth import HTTPBasicAuth
from flask_login import login_user
from app.models import Operator, InvalidUsage
import random
from app.operator import operator_blueprint
from sqlalchemy.exc import IntegrityError
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



@operator_blueprint.route('/login', methods=['POST'])
def login():
    operator_name = request.json.get("operator_name", None)
    password = request.json.get("password", None)
    operator = Operator.query.filter(Operator.operator_name==operator_name).first()

    if operator is None or not operator.verify_password(password=password):
        return jsonify(status="fail", reason="no this user or password error", data=[])

    userInfo = {
        "id": operator.id,
        "username": operator.operator_name
    }
    token = jwtEncoding(userInfo)
    login_user(operator, remember=True)

    return jsonify(status="success", reason="", operator=operator.to_json(), token = token.decode())

"""
@api {POST} /login 登录账号(json数据)
@apiGroup operator

@apiParam (json) {String} operator_name 登录账号
@apiParam (json) {String} password 新的密码

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
        try:
            logout_user()
            return jsonify(status="success", reason="")
        except:
            abort(500)
"""
@api {GET} /logout 登出账号(json数据)
@apiGroup operator

@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} status 登出情况

@apiSuccessExample Success-Response:
    登出成功
    {
        "status":"success",
        "reason":''
    }
"""

@operator_blueprint.route('/operator/password', methods = ['PUT'])
def change_password():
    operator_name  =request.json['operator_name']
    password = "".join(random.sample('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',8))
    operator = Operator.query.filter(Operator.operator_name == operator_name).first()
    operator.password = password
    try:
        db.session.add(operator)
        db.session.commit()
    except IntegrityError as e:
        raise InvalidUsage(message=str(e), status_code=500)
    return jsonify({
        'status':'success',
        'reason':'',
        'new_password':password,
        'operator':operator.to_json()
    })

"""
@api {PUT} /operator/password 修改密码(json数据)
@apiGroup operator

@apiParam (json) {String} operator_name 操作员姓名

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
        "new_password":"新的密码"
        "status":"success",
        "reason":''
    }
    更改失败
    {
        "status":"fail",
        "reason":""
    }
"""
