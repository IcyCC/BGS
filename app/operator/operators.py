from . import operator_blueprint
import os
from marshmallow.exceptions import ValidationError
from app import db, mail
from flask import request, jsonify, g, url_for, current_app, make_response
from app.models import Operator
from sqlalchemy.exc import OperationalError
from flask_login import login_required, current_user, logout_user
from flask_mail import Mail, Message
import requests
from app.form_model import UserValidation
import json

def std_json(d):
    r = {}
    for k, v in d.items():
        r[k] = json.loads(v)
    return r

@operator_blueprint.route('/operators', methods = ['POST'])
def new_operator():
    params_dict = {
        'username': request.json.get('username', None),
        'password': request.json.get('password', None),
        'email': request.json.get('email', None)
    }
    try:
        UserValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status':'fail',
            'reason':str(e)
        })
    tel = request.json['tel']
    operator = Operator.query.filter(Operator.tel == tel).first()
    if operator:
        return jsonify({
            'status':'fail',
            'reason':'the tel or the mail has been used'
        })
    operator = Operator.from_json(request.json)
    try:
        db.session.add(operator)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':operator.to_json()
        })
    req = requests.session()
    try:
        res = req.get('http://www.baidu.com')
        if res.status_code != 200:
            return jsonify({
                'status': 'fail',
                'reason': 'the web does not connect to the outer net',
                'operators': []
            })
    except:
        return jsonify({
            'status': 'fail',
            'reason': 'the web does not connect to the outer net',
            'operators': []
        })
    msg = Message('Operator active', sender='1468767640@qq.com', recipients=['1468767640@qq.com'])
    host = 'http://101.200.52.233:8080'
    msg.body = 'the operator name is %s, the operator id is%id, the operator url is %s%s' % (
    operator.operator_name, operator.id, host, url_for('operator_blueprint.get_operator', id=operator.id))
    # mail.send(msg)
    try:
        mail.send(msg)
    except:
        return jsonify({
            'status': 'fail',
            'reason': 'the mail has been posted failed',
            'operators': []
        })
    try:
        operator.active = True
        db.session.add(operator)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e),
            'data': []
        })
    return jsonify({
        'operators':[operator.to_json()],
        'status':'success',
        'reason':'the data has been added'
    })

"""
@api {POST} /operators 新建操作者(医生)信息(json数据)并激活
@apiGroup operator
@apiName 新建操作者信息
@apiParam (params) {String} operator_name 医生姓名
@apiParam (params) {String} password 登录密码
@apiParam (params) {String} hospital 医院名称   
@apiParam (params) {String} office 科室
@apiParam (params) {String} lesion 分区
@apiParam (params) {String} tel 医生电话
@apiParam (params) {String} mail 医生邮箱

@apiSuccess {Array} operators 返回新增的医生数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        operators:[{
            "url":"医生地址",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名"
        }],
        "status":"success",
        "reason":"the data has been added"
    }
    电话已经被注册
    {
        "status":"fail",
        "reason":"the tel or the mail has been used"
    }
    未连接外网
    {
        'status': 'fail',
        'reason': 'the web does not connect to the outer net',
        'operators': []
    }
    邮件发送失败
    {
        'status': 'fail',
        'reason': 'the mail has been posted failed',
        'operators': []
    }
"""


@operator_blueprint.route('/operators')
@login_required
def get_operators():
    operators = Operator.query
    fields = [i for i in Operator.__table__.c._data]
    per_page = current_app.config['PATIENTS_PRE_PAGE']
    limit = None
    for k, v in std_json(request.args).items():
        if k in fields:
            operators = operators.filter_by(**{k: v})
        if k == 'per_page':
            per_page = v
        if k == 'limit':
            limit = v
    operators = operators.limit(limit).from_self() if limit is not None else operators.from_self()
    page = request.args.get('page', 1, type=int)
    pagination = operators.paginate(page, per_page=per_page, error_out=False)
    operators = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('operator.get_operators', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('operator.get_operators', page=page + 1)
    return jsonify({
        'operators': [operator.to_json() for operator in operators],
        'prev': prev,
        'next': next,
        'has_prev':pagination.has_prev,
        'has_next':pagination.has_next,
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'status': 'success',
        'reason': 'there are datas'
    })

"""
@api {GET} /operators 获取查询操作者(地址栏筛选)
@apiGroup operator
@apiName 获取查询查询操作者

@apiParam (params) {Number} limit 查询总数量
@apiParam (params) {Number} per_page 每一页的数量
@apiParam (params) {String} operator_name 医生姓名
@apiParam (params) {String} hospital 医院名称
@apiParam (params) {String} office 科室
@apiParam (params) {String} lesion 分区
@apiParam (params) {String} tel 医生电话
@apiParam (params) {String} mail 医生邮箱
@apiParam (params) {Number} limit 查询总数量
@apiParam (params) {Number} per_page 每一页的数量
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} operators 返回新增的医生数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "operators":[{
            "url":"医生地址",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "active":"是否被激活",
            "lesion":"医生分区",
            "operator_name":"医生姓名"
        }],
        "prev":"上一页地址",
        "next":"下一页地址",
        'has_prev':'是否有上一页',
        'has_next':'是否有下一页',
        'total': '查询总数量',
        'pages': '查询总页数',
        'per_page': '每一页的数量',
        'status': 'success',
        'reason': 'there are datas'
    }
"""



@operator_blueprint.route('/operators/<int:id>')
@login_required
def get_operator(id):
    operator = Operator.query.get_or_404(id)
    return jsonify({
        'operators': [operator.to_json()],
        'status': 'success',
        'reason': 'there is the data'
    })

"""
@api {GET} /operators/<int:id> 根据id查询操作者
@apiGroup operator
@apiName 根据id查询操作者

@apiParam (params) {Number} id 医生id
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} operators 返回新增的医生数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        operators:[{
            "url":"医生地址",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名"
        }],
        "status":"success",
        "reason":"there is the data"
    }
    @apiError (Error 4xx) 404 对应id的医生不存在

    @apiErrorExample Error-Resopnse:
    HTTP/1.1 404 对应id的医生不存在 
"""

@operator_blueprint.route('/operators/<int:id>', methods = ['DELETE'])
@login_required
def delete_operator(id):
    operator = Operator.query.get_or_404(id)
    if current_user.tel != operator.tel:
        return jsonify({
            'status':'fail',
            'reason':'no root'
        }), 403
    try:
        db.session.delete(operator)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':operator.to_json()
        })
    return jsonify({
        'operators': [operator.to_json()],
        'status': 'success',
        'reason': 'the data has been deleted'
    }), 200

"""
@api {DELETE} /operators/<int:id> 根据id删除操作者
@apiGroup operator
@apiName 根据id删除操作者

@apiParam (params) {Number} id 医生id
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} operators 返回删除的医生数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        operators:[{
            "url":"医生地址",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名"
        }],
        "status":"success",
        "reason":"the data has been deleted"
    }
    不是本人删除
    {
        "status":"fail",
        "root":"no root"
    }
    @apiError (Error 4xx) 404 对应id的医生不存在

    @apiErrorExample Error-Resopnse:
    HTTP/1.1 404 对应id的医生不存在 
"""


@operator_blueprint.route('/operators/<int:id>', methods = ['PUT'])
@login_required
def change_operator(id):
    operator = Operator.query.get_or_404(id)
    for k in request.json:
        if hasattr(operator, k):
            setattr(operator, k, request.json[k])
        if k == 'password':
            operator.password =  request.json[k]
    try:
        db.session.add(operator)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e
        })
    return jsonify({
        'operators': [operator.to_json()],
        'status': 'success',
        'reason': 'the data has been changed'
    }), 200

"""
@api {PUT} /operators/<int:id> 根据id修改操作者信息(json数据)
@apiGroup operator
@apiName 根据id修改操作者信息

@apiParam (params) {Number} id 医生id
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} operators 返回修改后的的医生数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        operators:[{
            "url":"医生地址",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名"
        }],
        "status":"success",
        "reason":"the data has been changed"
    }
    不是本人修改
    {
        "status":"fail",
        "reason":""
    }
    @apiError (Error 4xx) 404 对应id的医生不存在

    @apiErrorExample Error-Resopnse:
    HTTP/1.1 404 对应id的医生不存在 
"""


@operator_blueprint.route('/current_operator')
@login_required
def get_operator_now():
    operator = current_user
    return jsonify({
        'operators': [operator.to_json()],
        'status': 'success',
        'reason': 'there is the data'
    })

"""
@api {GET} /current_operator 返回现在操作者的信息
@apiGroup operator
@apiName 返回现在操作者的信息

@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} operators 返回现在操作者的信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        operators:[{
            "url":"医生地址",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名"
        }],
        "status":"success",
        "reason":"there is the data"
    } 
"""


@operator_blueprint.route('/current_operator/password', methods = ['POST'])
@login_required
def operator_password():
    operator_name = None
    password = ''
    if 'password' in request.json:
        password = request.json.get('password')
    if 'operator_name' in request.cookies:
        operator_name = request.cookies.get('operator_name')
        password = request.cookies.get('password')
    operator = current_user if operator_name is None else Operator.query.filter(Operator.operator_name == operator_name).first()
    if operator.verify_password(password):
        json = {
            'operators': [operator.to_json()],
            'status': 'success',
            'reason': 'the password is right'
        }
        return jsonify(json)
    else:
        return jsonify({
            'status':'fail',
            'reason':'wrong password'
        })

"""
@api {GET} /current_operator/password 验证现在操作者输入密码是否正确
@apiGroup operator
@apiName 验证现在操作者输入密码是是否正确

@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} operators 返回现在操作者的信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        operators:[{
            "url":"医生地址",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名"
        }],
        "status":"success",
        "reason":"the password is right"
    }
    密码错误
    {
        "status":"fail",
        "reason":"wrong password"
    } 
"""

