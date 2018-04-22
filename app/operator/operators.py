from app.gencode import api
import os
from app import db
from flask import request, jsonify, g, url_for, current_app, make_response
from app.models import Operator
from .authentication import auth
from sqlalchemy.exc import OperationalError
from flask_login import login_required, current_user, logout_user
@api.route('/operators', methods = ['POST'])
def new_operator():
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
    return jsonify({
        'operators':[operator.to_json()],
        'status':'success',
        'reason':'the data has been added'
    })

"""
@api {POST} /operator/operators 新建操作者(医生)信息(json数据)
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
"""


@api.route('/operators')
@login_required
def get_operators():
    operators = Operator.query
    fields = [i for i in Operator.__table__.c._data]
    for k, v in request.args.items():
        if k in fields:
            operators = operators.filter_by(**{k: v})
    if operators.count()!=0:
        page = request.args.get('page', 1, type=int)
        pagination = operators.paginate(page, per_page=current_app.config['PATIENTS_PRE_PAGE'], error_out=False)
        operators = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.get_operators', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('api.get_operators', page=page + 1)
        return jsonify({
            'operators': [operator.to_json() for operator in operators],
            'prev': prev,
            'next': next,
            'count': pagination.total,
            'pages':pagination.pages,
            'status':'success',
            'reason':'there are the datas'
        })
    else:
        return jsonify({
            'status': 'fail',
            'reason': 'there is no data'
        })

"""
@api {GET} /operator/operators 获取查询操作者(地址栏筛选)
@apiGroup operator
@apiName 获取查询查询操作者

@apiParam (params) {String} operator_name 医生姓名
@apiParam (params) {String} hospital 医院名称
@apiParam (params) {String} office 科室
@apiParam (params) {String} lesion 分区
@apiParam (params) {String} tel 医生电话
@apiParam (params) {String} mail 医生邮箱
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} operators 返回新增的医生数据

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
        "count":"总数量",
        "prev":"上一页地址",
        "next":"下一页地址",
        "pages":"总页数",
        "status":"success",
        "reason":"there are the datas"
    }
    没有数据
    {
        "status"："fail",
        "reason":"there is no data"
    }
"""



@api.route('/operators/<int:id>')
@login_required

def get_operator(id):
    operator = Operator.query.get_or_404(id)
    return jsonify({
        'operators': [operator.to_json()],
        'status': 'success',
        'reason': 'there is the data'
    })

"""
@api {GET} /operator/operators/<int:id> 根据id查询操作者
@apiGroup operators
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

@api.route('/operators/<int:id>', methods = ['DELETE'])
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
@api {DELETE} /operator/operators/<int:id> 根据id删除操作者
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


@api.route('/operators/<int:id>', methods = ['PUT'])

def change_operator(id):
    operator = Operator.query.get_or_404(id)
    if current_user.tel != operator.tel:
        return jsonify({
            'status': 'fail',
            'reason': 'no root'
        }), 403
    for k in request.json:
        if hasattr(operator, k):
            setattr(operator, k, request.json[k])
    if 'password' in request.json:
        password = request.json['password']
        operator.password = password
    try:
        db.session.add(operator)
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
        'reason': 'the data has been changed'
    }), 200

"""
@api {PUT} /operator/operators/<int:id> 根据id修改操作者信息(json数据)
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
        "root":"no root"
    }
    @apiError (Error 4xx) 404 对应id的医生不存在

    @apiErrorExample Error-Resopnse:
    HTTP/1.1 404 对应id的医生不存在 
"""


@api.route('/now')
@login_required
def get_operator_now():
    operator = current_user
    return jsonify({
        'operators': [operator.to_json()],
        'status': 'success',
        'reason': 'there is the data'
    })

"""
@api {GET} /operator/now 返回现在操作者的信息
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


@api.route('/now/password', methods = ['POST'])
@login_required

def operator_password():
    operator_name = ''
    if 'password' in request.json:
        password = request.json.get('password')
    if 'operator_name' in request.cookies:
        operator_name = request.cookies.get('operator_name')
        password = request.cookies.get('password')
    if operator_name is None:
        print('sssss')
    operator = current_user if operator_name is '' else Operator.query.filter(Operator.operator_name == operator_name).first()
    if operator.verify_password(password):
        json = {
            'operators': [operator.to_json()],
            'status': 'success',
            'reason': 'the password is right'
        }
        res = make_response(jsonify(json))
        res.set_cookie('operator_name', operator.operator_name,max_age=60)
        res.set_cookie('password', password, max_age=60)
        return res
    else:
        return jsonify({
            'status':'fail',
            'reason':'wrong password'
        })

"""
@api {GET} /operator/now/password 验证现在操作者输入密码是否正确
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

@api.route('/change_password', methods = ['POST'])
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
@api {POST} /operator/operators 新建操作者(医生)信息(json数据)
@apiGroup operator
@apiName 新建操作者信息
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