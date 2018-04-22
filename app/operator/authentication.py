from flask import g, jsonify, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_login import login_user
from app.models import Operator
import requests
from app.operator import operator
from sqlalchemy.exc import OperationalError
from flask_login import current_user, login_required, logout_user
from flask_mail import Mail, Message
from app import mail, db
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
"""
用于判断密码是否正确
"""

@operator.route('/active')

def operator_active():
    req = requests.session()
    try:
        res = req.get('http://www.baidu.com')
        if res.status_code !=200:
            return jsonify({
                'status':'fail',
                'reason':'the web does not connect to the outer net',
                'operators': []
            })
    except:
        return jsonify({
            'status': 'fail',
            'reason': 'the web does not connect to the outer net',
            'operators': []
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
            'operators':[]
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
        'operators':[operator.to_json()]
    })

"""
@api {GET} /operator/active 用于激活账号（需要服务器支持使stmp）
@apiGroup authentication

@apiSuccess {Array} status 返回账号是否激活成功
@apiSuccess {Array} operators 返回激活成功的账号信息

@apiSuccessExample Success-Response:
    激活成功
    {
        "status":"success",
        "reason":"the operator has been actived",
        "operators":[{
            "url":"医生地址",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名"
        }]
    }
    激活失败
    {
        "status":"fail",
        "reason":"",
        "operators":[]
    }
"""


@operator.route('/tokens')
@auth.login_required
def get_auth_token():
    token = g.current_user.generate_auth_token()
    return jsonify({
        'token':token,
        'status':'fail',
        'reason':'the token has been gotten'
    })

"""
@api {GET} /operator/tokens 根据登陆的账号密码获得token
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

@operator.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    operator = Operator.query.filter(Operator.operator_name==username).first()

    if operator is None or not operator.verify_password(password=password):
        return jsonify(status="fail", reason="no this user or password error", data=[])

    login_user(operator, remember=True)

    return jsonify(status="success", reason="", operators=[operator.to_json()])

"""
@api {POST} /operator/login 登录账号(json数据)
@apiGroup operator
@apiName 新建操作者信息
@apiParam (params) {String} hospital 医院名称
@apiParam (params) {String} office 科室
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
        "reason":''
    }
    更改失败
    {
        "status":"fail",
        "reason":"",
        "operators":[]
    }
"""


@operator.route("/logout", methods=["GET"])
@login_required
def logout():
    if request.method == "GET":
        logout_user()
        return jsonify(status="success", reason="", operators=[])

"""
@api {GET} /operator/logout 登出账号(json数据)
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


