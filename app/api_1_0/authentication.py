from flask import g, jsonify, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_login import login_user
from ..models import Operator
import requests
from . import api
from sqlalchemy.exc import OperationalError
from flask_login import current_user, login_required, logout_user
from ..decorators import allow_cross_domain
from flask_mail import Mail, Message
from .. import mail, db
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

@api.route('/active')
@allow_cross_domain
def operator_active():
    req = requests.session()
    try:
        res = req.get('http://www.baidu.com')
        if res.status_code !=200:
            return jsonify({
                'status':'fail',
                'reason':'the web does not connect to the outer net'
            })
    except:
        return jsonify({
            'status': 'fail',
            'reason': 'the web does not connect to the outer net'
        })
    name = request.args['name']
    operator = Operator.query.filter(Operator.operator_name == name).first()
    msg = Message('Operator active', sender='1468767640@qq.com', recipients=['1468767640@qq.com'])
    host = 'http://101.200.52.233:8080'
    msg.body = 'the operator name is %s, the operator id is%id, the operator url is %s%s'%(operator.operator_name, operator.id, host, url_for('api.get_operator', id=operator.id))
    try:
        mail.send(msg)
    except:
        return jsonify({
            'status':'fail',
            'reason':'the mail has been posted failed',
            'data':[]
        })
    try:
        operator.active = True
        db.session.add(operator)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':str(e),
            'data':[]
        })
    return jsonify({
        'status':'success',
        'reason':'the operator has been actived',
        'data':[operator.to_json()]
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
@allow_cross_domain
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

@api.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    operator = Operator.query.filter(Operator.operator_name==username).first()

    if operator is None or not operator.verify_password(password=password):
        return jsonify(status="fail", reason="no this user or password error", data=[])

    if operator.active is not True:
        return jsonify({
            'status':'fail',
            'reason':'the user does not been actived'
        })

    login_user(operator, remember=False)

    return jsonify(status="success", reason="", data=[operator.to_json()])

@api.route("/logout", methods=["GET"])
@login_required
def logout():
    if request.method == "GET":
        logout_user()
        return jsonify(status="success", reason="", data=[])


