from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for, current_app
from ..models import Patient, Operator, Data, Bed, Accuchek
from .authentication import auth
from sqlalchemy.exc import OperationalError,IntegrityError
from ..decorators import allow_cross_domain
from flask_login import login_required

@api.route('/accucheks')
@login_required
@allow_cross_domain
def get_accunckes():
    fields = [i for i in Accuchek.__table__.c._data]
    accunckes = Accuchek.query
    for k, v in request.args.items():
        if k in fields:
            accunckes = accunckes.filter_by(**{k: v})
    if accunckes.count()!=0:
        page = request.args.get('page', 1, type=int)
        pagination = accunckes.paginate(page, per_page=current_app.config['PATIENTS_PRE_PAGE'], error_out=False)
        accunckes = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.get_patients', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('api.get_patients', page=page + 1)
        return jsonify({
            'accunckes': [accuncke.to_json() for accuncke in accunckes],
            'prev': prev,
            'next': next,
            'count': pagination.total,
            'pages': pagination.pages,
            'status':'success',
            'reason':'there are datas'
        })
    else:
        return jsonify({
            'status':'fail',
            'reason':'there is no data'
        }), 404

"""
@api {GET} /api/v1.0/accucheks 获取所有血糖仪信息(地址栏筛选)
@apiGroup accucheks
@apiName 获取所有血糖仪信息

@apiParam (params) {String} sn 血糖仪sn码
@apiParam (params) {Number} bed_id 病床号码
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} accucheks 返回所有根据条件查询到的血糖仪信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "accuncheks":[{
            "url":"血糖仪地址",
            "sn":"血糖仪sn码",
            "bed_id":"床位号"
        }](血糖仪信息),
        "prev":"上一页地址",
        "next":"下一页地址",
        "count":"总数量",
        "pages":"总页数",
        "status":"success",
        "reason":"there are datas"
    }
    没有数据
    {
        "status":"fail",
        "reason":"there is no data"
    }
"""

@api.route('/accucheks', methods = ['POST'])
@login_required
@allow_cross_domain
def new_accuchek():
    accuchek = Accuchek()
    if 'sn' in request.json:
        sn = request.json['sn']
        may_accuchek = Accuchek.query.filter(Accuchek.sn == sn).first()
        if may_accuchek:
            return jsonify({
                'status':'fail',
                'reason':'the sn has been used'
            })
    for k in request.json:
        if hasattr(accuchek, k):
            try:
                setattr(accuchek, k, request.json[k])
            except IntegrityError as e:
                return jsonify({
                    'status':'fail',
                    'reason':e
                })
    try:
        db.session.add(accuchek)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':accuchek.to_json()
        })
    return jsonify({
        "accukces":[accuchek.to_json()],
        "status":"success",
        "reason":"the data has been added"
    })

"""
@api {POST} /api/v1.0/accucheks 添加一个新的血糖仪(json数据)
@apiGroup accucheks
@apiName 添加一个血糖仪

@apiParam (params) {String} sn 血糖仪sn码
@apiParam (params) {Number} bed_id 病床号码
@apiParam (Login) {String} login 登录才可以访问 

@apiSuccess {Array} accucheks 返回添加血糖仪的信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "accucheks":[{
            "bed_id":"床位号",
            "sn":"血糖仪sn码",
            "url":"血糖仪地址"   
        }],
        "status":"success",
        "reason":"the data has been added"
    }
    {
        "status":"fail",
        "reason":"失败原因"
    }
"""

@api.route('/accucheks/<int:id>')
@login_required
@allow_cross_domain
def get_accuchek(id):
    accuchek = Accuchek.query.get_or_404(id)
    return jsonify({
        "accukces":[accuchek.to_json()],
        "status":"success",
        "reason":"there is the data"
    })

"""
@api {GET} /api/v1.0/accucheks/<int:id> 根据id获取血糖仪信息
@apiGroup accucheks
@apiName 根据id获取血糖仪信息

@apiParam (params) {Number} id 血糖仪id
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} accucheks 返回相应血糖仪的信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "accucheks":[{
            "bed_id":"床位号",
            "sn":"血糖仪sn码",
            "url":"血糖仪地址"   
        }],
        "status":"success",
        "reason":"there is the data"
    }

@apiError (Error 4xx) 404 对应id的血糖仪不存在

@apiErrorExample Error-Resopnse:
    HTTP/1.1 404 对应的血糖仪信息不存在
"""

@api.route('/accucheks/<int:id>', methods = ['DELETE'])
@login_required
@allow_cross_domain
def delete_accuchek(id):
    accuchek = Accuchek.query.get_or_404(id)
    try:
        db.session.delete(accuchek)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e
        })
    return jsonify({
        "accukces": [accuchek.to_json()],
        "status": "success",
        "reason": "the data has been deleted"
    })

"""
@api {DELETE} /api/v1.0/accucheks/<int:id> 删除id所代表的血糖仪
@apiGroup accucheks
@apiName 删除id所代表的血糖仪

@apiParam (params) {Number} id 血糖仪id
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} accucheks 返回被删除的血糖仪的信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "accucheks":[{
            "bed_id":"床位号",
            "sn":"血糖仪sn码",
            "url":"血糖仪地址"   
        }],
        "status":"success",
        "reason":"the data has been deleted"
    }

@apiError (Error 4xx) 404 对应id的血糖仪不存在

@apiErrorExample Error-Resopnse:
    HTTP/1.1 404 对应的血糖仪信息不存在
"""

@api.route('/accucheks/<int:id>', methods = ['PUT'])
@login_required

def change_accuchek(id):
    accuchek = Accuchek.query.get_or_404(id)
    if 'sn' in request.json:
        sn = request.json['sn']
        may_accuchek = Accuchek.query.filter(Accuchek.sn == sn).first()
        if may_accuchek.accuchek_id != id:
            return jsonify({
                'status':'fail',
                'reason':'the sn has been used'
            })
    for k in request.json:
        if hasattr(accuchek, k):
            setattr(accuchek, k, request.json[k])
    try:
        db.session.add(accuchek)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e
        })
    return jsonify({
        "accukces": [accuchek.to_json()],
        "status": "success",
        "reason": "the data has been changed"
    })

"""
@api {PUT} /api/v1.0/accucheks/<int:id> 更改id所代表的血糖仪的信息(json数据)
@apiGroup accucheks
@apiName 更改id所代表的血糖仪的信息

@apiParam (params) {Number} id 血糖仪id
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} accucheks 返回更改后的血糖仪的信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "accucheks":[{
            "bed_id":"床位号",
            "sn":"血糖仪sn码",
            "url":"血糖仪地址"   
        }],
        "status":"success",
        "reason":"the data has been changed"
    }


@apiError (Error 4xx) 404 对应id的血糖仪不存在

@apiErrorExample Error-Resopnse:
    HTTP/1.1 404 对应的血糖仪信息不存在
"""


