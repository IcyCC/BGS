from . import operator_blueprint
import os
from marshmallow.exceptions import ValidationError
from app import db, mail
from flask import request, jsonify, g, url_for, current_app, make_response
from app.models import Operator
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, current_user, logout_user
from flask_mail import Mail, Message
import requests
from app.models import InvalidUsage
from app.form_model import OperatorValidation, ChangeOperatorValidation, GetOperatorValidation, OperatorPasswordValidation
import json

def std_json(d):
    r = {}
    for k, v in d.items():
        try:
            r[k] = json.loads(v)
        except:
            r[k] = v
    return r

@operator_blueprint.route('/operators', methods = ['POST'])
def new_operator():
    params_dict = {
        'operator_id': request.json.get('operator_id', None),
        'operator_name': request.json.get('operator_name', None),
        'password': request.json.get('password', None),
        'tel': request.json.get('tel', None),
        'hospital': request.json.get('hospital', None),
        'lesion': request.json.get('lesion', None),
        'email': request.json.get('email', None),
        'office':request.json.get('office', None)
    }
    try:
        OperatorValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status':'fail',
            'reason':str(e)
        })
    if 'tel'  not in request.json or request.json['tel'] is None:
        return jsonify({
            'status':'fail',
            'reason':'需要有电话'
        })
    if 'operator_name'  not in request.json or request.json['operator_name'] is None:
        return jsonify({
            'status':'fail',
            'reason':'需要有账户名'
        })
    tel = request.json['tel']
    operator_name = request.json['operator_name']
    operator = Operator.query.filter(Operator.operator_name == operator_name).first()
    if operator:
        return jsonify({
            'status':'fail',
            'reason':'用户名已经被使用了'
        })
    operator = Operator.query.filter(Operator.tel == tel).first()
    if operator:
        return jsonify({
            'status':'fail',
            'reason':'电话或者邮箱已经被使用了'
        })
    operator = Operator.from_json(request.json)
    # req = requests.session()
    # try:
    #     res = req.get('http://www.baidu.com')
    #     if res.status_code != 200:
    #         return jsonify({
    #             'status': 'fail',
    #             'reason': 'the web does not connect to the outer net',
    #             'operators': []
    #         })
    # except:
    #     return jsonify({
    #         'status': 'fail',
    #         'reason': 'the web does not connect to the outer net',
    #         'operators': []
    #     })
    # msg = Message('Operator active', sender='1468767640@qq.com', recipients=['1468767640@qq.com'])
    # host = 'http://101.200.52.233:8080'
    # msg.body = 'the operator name is %s, the operator id is%id, the operator url is %s%s' % (
    # operator.operator_name, operator.id, host, url_for('operator_blueprint.get_operator', id=operator.id))
    # # mail.send(msg)
    # try:
    #     mail.send(msg)
    # except:
    #     return jsonify({
    #         'status': 'fail',
    #         'reason': 'the mail has been posted failed',
    #         'operators': []
    #     })
    try:
        db.session.add(operator)
        db.session.commit()
    except IntegrityError as e:
        raise InvalidUsage(message=str(e), status_code=500)
    return jsonify({
        'operator':operator.to_json(),
        'status':'success',
        'reason':'数据已经被添加'
    })

"""
@api {POST} /operators 新建操作者(医生)信息(json数据)并激活
@apiGroup operator

@apiParam (json) {String} operator_name 医生姓名
@apiParam (json) {String} password 登录密码
@apiParam (json) {String} hospital 医院名称   
@apiParam (json) {String} office 科室
@apiParam (json) {String} lesion 分区
@apiParam (json) {String} tel 医生电话
@apiParam (json) {String} mail 医生邮箱

@apiSuccess {Array} operators 返回新增的医生数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "operator":{
            "operator_id":"医生id",
            "mail":"医生邮箱",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名".
            "tel":"医生电话"
        },
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
    params_dict = {
        'operator_id': request.args.get('operator_id', None, type=id),
        'operator_name': request.args.get('operator_name', None),
        'password': request.args.get('password', None),
        'tel': request.args.get('tel', None),
        'hospital': request.args.get('hospital', None),
        'lesion': request.args.get('lesion', None),
        'email': request.args.get('email', None),
        'office': request.args.get('office', None),
        'limit': request.args.get('limit', None, type= int),
        'per_page': request.args.get('per_page', None, type=int)
    }
    try:
        GetOperatorValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
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
        'operator': [operator.to_json() for operator in operators],
        'prev': prev,
        'next': next,
        'has_prev':pagination.has_prev,
        'has_next':pagination.has_next,
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'status': 'success',
        'reason': '这里是查询到的数据'
    })

"""
@api {GET} /operators 获取查询操作者(地址栏筛选)
@apiGroup operator

@apiParam (params) {Int} operator_id 操作者id
@apiParam (params) {String} operator_name 医生姓名
@apiParam (params) {String} hospital 医院名称
@apiParam (params) {String} office 科室
@apiParam (params) {String} lesion 分区
@apiParam (params) {String} tel 医生电话
@apiParam (params) {String} mail 医生邮箱
@apiParam (params) {Int} limit 查询总数量
@apiParam (params) {Int} per_page 每一页的数量
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} operators 返回新增的医生数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "operators":[{
            "operator_id":"医生id",
            "mail":"医生邮箱",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名".
            "tel":"医生电话"
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
        'operators': operator.to_json(),
        'status': 'success',
        'reason': '这里是查询到的数据'
    })

"""
@api {GET} /operators/<int:id> 根据id查询操作者
@apiGroup operator

@apiParam (params) {Int} id 医生id
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} operators 返回新增的医生数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "operator":{
            "operator_id":"医生id",
            "mail":"医生邮箱",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名".
            "tel":"医生电话"
        },
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
            'reason':'没有权限'
        }), 403
    try:
        db.session.delete(operator)
        db.session.commit()
    except IntegrityError as e:
        raise InvalidUsage(message=str(e), status_code=500)
    return jsonify({
        'status': 'success',
        'reason': '数据已经被删除了'
    }), 200

"""
@api {DELETE} /operators/<int:id> 根据id删除操作者
@apiGroup operator

@apiParam (params) {Int} id 医生id
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} operators 返回删除的医生数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
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
    params_dict = {
        'operator_id': request.json.get('operator_id', None),
        'operator_name': request.json.get('operator_name', None),
        'password': request.json.get('password', None),
        'tel': request.json.get('tel', None),
        'hospital': request.json.get('hospital', None),
        'lesion': request.json.get('lesion', None),
        'email': request.json.get('email', None),
        'office': request.json.get('office', None)
    }
    try:
        ChangeOperatorValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    operator = Operator.query.get_or_404(id)
    for k in request.json:
        if k == 'password_hash':
            continue
        if k == 'password':
            operator.password =  request.json[k]
        if hasattr(operator, k):
            setattr(operator, k, request.json[k])
    try:
        db.session.add(operator)
        db.session.commit()
    except IntegrityError as e:
        raise InvalidUsage(message=str(e), status_code=500)
    return jsonify({
        'operator': operator.to_json(),
        'status': 'success',
        'reason': '数据已经被更改了'
    }), 200

"""
@api {PUT} /operators/<int:id> 根据id修改操作者信息(json数据)
@apiGroup operator

@apiParam (params) {Int} id 医生id
@apiParam (json) {String} tel 电话号码
@apiParam (json) {String} hospital 医院名称
@apiParam (json) {String} lesion 医生分区
@apiParam (json) {String} email 电子邮箱
@apiParam (json) {String} office 医生科室 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} operators 返回修改后的的医生数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "operator":{
            "operator_id":"医生id",
            "mail":"医生邮箱",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名".
            "tel":"医生电话"
        },
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


@operator_blueprint.route('/operators/current')
@login_required
def get_operator_now():
    operator = current_user
    return jsonify({
        'operator': operator.to_json(),
        'status': 'success',
        'reason': '这里是正在使用的用户'
    })

"""
@api {GET} /operators/current 返回现在操作者的信息
@apiGroup operator

@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} operators 返回现在操作者的信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "operator":{
            "operator_id":"医生id",
            "mail":"医生邮箱",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名".
            "tel":"医生电话"
        },
        "status":"success",
        "reason":"there is the data"
    } 
"""


@operator_blueprint.route('/operators/current/password', methods = ['POST'])
@login_required
def operator_password():
    params_dict = {
        'operator_name': request.json.get('operator_name', None),
        'password': request.json.get('password', None)
    }
    try:
        OperatorPasswordValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
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
            'operator': operator.to_json(),
            'status': 'success',
            'reason': '密码正确'
        }
        return jsonify(json)
    else:
        return jsonify({
            'status':'fail',
            'reason':'密码错误'
        })

"""
@api {POST} /operators/current/password 验证现在操作者输入密码是否正确
@apiGroup operator

@apiParam (json) {String} password 登录密码
@apiParam (json) {String} operator_name 操作者姓名
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} operators 返回现在操作者的信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "operator":{
            "operator_id":"医生id",
            "mail":"医生邮箱",
            "hospital":"医生医院名称",
            "office":"医生科室",
            "lesion":"医生分区",
            "operator_name":"医生姓名".
            "tel":"医生电话"
        },
        "status":"success",
        "reason":"the password is right"
    }   
    密码错误
    {
        "status":"fail",
        "reason":"wrong password"
    } 
"""

