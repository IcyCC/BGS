from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for, current_app
from ..models import Patient, Operator, Data, Bed, Accuchek
from .authentication import auth
import datetime
from sqlalchemy.exc import OperationalError
from ..decorators import allow_cross_domain
from .authentication import auth

@api.route('/datas/auto', methods=['POST'])

@allow_cross_domain
def new_data_auto():
    data = Data()
    for k in request.json:
        if hasattr(data, k):
            setattr(data, k, request.json[k])
    accuchek = Accuchek.query.filter(Accuchek.sn == request.json['sn']).first()
    bed = accuchek.bed
    patient = bed.patient
    id_number = patient.id_number
    data.id_number = id_number
    try:
        db.session.add(data)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'reason': e,
            'data': data.to_json()
        })
    return jsonify({
        'datas': [data.to_json()],
        'status': 'success',
        'reason': 'the data has been added'
    })


"""
@api {POST} /api/v1.0/datas/auto 添加数据(不用手动输入病人数据)(json数据)
@apiGroup datas
@apiName 添加数据

@apiParam (params) {String} sn 血糖仪sn码 
@apiParam (params) {String} date 数据日期_日期格式(0000-00-00)
@apiParam (params) {String} time 数据时间_时间格式(00:00:00)
@apiParam (params) {Number} glucose 血糖值
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回新添加的数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "datas":[{
            "date":"数据添加日期",
            "time":"数据添加时间",
            "id_number":"医疗卡号",
            "patient":"病人地址",
            "sn":"血糖仪sn码",
            "url":"数据地址"
        }],
        "status":"success",
        "reason":"the data has been added"
    } 
"""


@api.route('/datas/artificial', methods=['POST'])

@allow_cross_domain
def new_data_artificial():
    data = Data()
    for k in request.json:
        if hasattr(data, k):
            setattr(data, k, request.json[k])
    id_number = request.json['id_number']
    patient = Patient.query.filter(Patient.id_number == id_number).first()
    if patient is None:
        patient = Patient()
    for k in request.json:
        if hasattr(patient, k):
            setattr(patient, k, request.json[k])
    try:
        db.session.add(patient)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'reason': e,
            'data': data.to_json()
        })
    try:
        db.session.add(data)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'reason': e,
            'data': data.to_json()
        })
    return jsonify({
        'datas': [data.to_json()],
        'status': 'success',
        'reason': 'the data has been added'
    })


"""
@api {POST} /api/v1.0/datas/artificial 添加数据(不用手动输入病人数据)(json数据)
@apiGroup datas
@apiName 添加数据

@apiParam (params) {String} id_number 医疗卡号
@apiParam (params) {String} patient_name 病人姓名
@apiParam (params) {String} sex 病人性别
@apiParam (params) {String} tel 病人电话
@apiParam (params) {Number} age 病人年龄
@apiParam (params) {Number} doctor_id 医生id
@apiParam (params) {String} sn 血糖仪sn码 
@apiParam (params) {String} date 数据日期_日期格式(0000-00-00)
@apiParam (params) {String} time 数据时间_时间格式(00:00:00)
@apiParam (params) {Number} glucose 血糖值
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回新添加的数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "datas":[{
            "date":"数据添加日期",
            "time":"数据添加时间",
            "id_number":"医疗卡号",
            "patient":"病人地址",
            "sn":"血糖仪sn码",
            "url":"数据地址"
        }],
        "status":"success",
        "reason":"the data has been added"
    }  
"""


@api.route('/datas')

@allow_cross_domain
def get_datas():
    data_fields = [i for i in Data.__table__.c._data]
    fields = data_fields
    datas = Data.query
    for k, v in request.args.items():
        if k in fields:
            datas = datas.filter_by(**{k: v})
    if datas.count() != 0:
        page = request.args.get('page', 1, type=int)
        pagination = datas.paginate(page, per_page=current_app.config['PATIENTS_PRE_PAGE'], error_out=False)
        datas = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.get_patients', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('api.get_patients', page=page + 1)
        return jsonify({
            'datas': [data.to_json() for data in datas],
            'prev': prev,
            'next': next,
            'count': pagination.total,
            'pages': pagination.pages,
            'status': 'success',
            'reason': 'there are the reasons'
        })
    else:
        return jsonify({
            'status': 'fail',
            'reason': 'there is no data'
        })


"""
@api {GET} /api/v1.0/datas 获取所有数据信息
@apiGroup datas
@apiName 获取所有数据信息

@apiParam (params) {String} sn 血糖仪sn码 
@apiParam (params) {String} date 数据日期_日期格式(0000-00-00)
@apiParam (params) {String} time 数据时间_时间格式(00:00:00)
@apiParam (params) {Number} glucose 血糖值
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回新添加的数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "datas":[{
            "date":"数据添加日期",
            "time":"数据添加时间",
            "id_number":"医疗卡号",
            "patient":"病人地址",
            "sn":"血糖仪sn码",
            "url":"数据地址"
        }],
        "count":"总数量",
        "prev":"上一页地址",
        "next":"下一页地址".
        "pages":'总页数",
        "status":"success",
        "reason":"there are the datas"
    }
    没有数据
    {
        "status":"fail",
        "reason":"there is no data"
    } 

"""


@api.route('/datas/<int:id>')

@allow_cross_domain
def get_data(id):
    data = Data.query.get_or_404(id)
    return jsonify({
        'datas': [data.to_json()],
        'status': 'success',
        'reason': 'the data has been added'
    })


"""
@api {GET} /api/v1.0/datas/<int:id> 根据id获取数据信息
@apiGroup datas
@apiName 根据id获取数据信息

@apiParam (params) {String} id 数据id 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回id所代表数据信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "datas":[{
            "date":"数据添加日期",
            "time":"数据添加时间",
            "id_number":"医疗卡号",
            "patient":"病人地址",
            "sn":"血糖仪sn码",
            "url":"数据地址"
        }],
        "status":"success",
        "reason":"there is the data"
    }

"""


@api.route('/datas/<int:id>', methods=['PUT'])

@allow_cross_domain
def change_data(id):
    data = Data.query.get_or_404(id)
    if g.current_user.operator_id != data.patient.doctor_id:
        return jsonify({
            'status': 'fail',
            'reason': 'no root'
        })
    id_number = data.id_number
    if 'id_number' in request.json:
        id_number = request.json['id_number']
    for k in request.json:
        if hasattr(data, k):
            setattr(data, k, request.json[k])
    patient = Patient.query.filter(Patient.id_number == id_number).first()
    try:
        db.session.add(data)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'reason': e,
            'data': data.to_json()
        })
    return jsonify({
        'datas': [{
            'url': url_for('api.get_data', id=data.data_id),
            'patient': url_for('api.get_patient', id=patient.patient_id),
            'sn': data.sn,
            'id_number': data.id_number,
            'time': str(data.time),
            'date': str(data.date),
            'glucose': data.glucose
        }],
        'status': 'success',
        'reason': 'the data has been changed'
    }), 200


"""
@api {PUT} /api/v1.0/datas/<int:id> 更改id所代表的数据的信息
@apiGroup datas
@apiName 更改id所代表的数据的信息

@apiParam (params) {String} id_number 医疗卡号(修改病人信息时添加)
@apiParam (params) {String} patient_name 病人姓名(修改病人信息时添加)
@apiParam (params) {String} sex 病人性别(修改病人信息时添加)
@apiParam (params) {String} tel 病人电话(修改病人信息时添加)
@apiParam (params) {Number} age 病人年龄(修改病人信息时添加)
@apiParam (params) {Number} doctor_id 医生id(修改病人信息时添加)
@apiParam (params) {String} sn 血糖仪sn码 
@apiParam (params) {String} date 数据日期_日期格式(0000-00-00)
@apiParam (params) {String} time 数据时间_时间格式(00:00:00)
@apiParam (params) {Number} glucose 血糖值
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回id所代表数据信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "datas":[{
            "date":"数据添加日期",
            "time":"数据添加时间",
            "id_number":"医疗卡号",
            "patient":"病人地址",
            "sn":"血糖仪sn码",
            "url":"数据地址"
        }],
        "status":"success",
        "reason":"the data has been changed"
    }
    不是本人主任医生修改
    {
        "status":"fail",
        "reason":"no root"
    }
"""


@api.route('/datas/<int:id>', methods=['DELETE'])

@allow_cross_domain
def delete_data(id):
    data = Data.query.get_or_404(id)
    if g.current_user.operator_id != data.patient.doctor_id:
        return jsonify({
            'status': 'fail',
            'reason': 'no root'
        })
    patient = data.patient
    try:
        db.session.delete(data)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'reason': e,
            'data': data.to_json()
        })
    return jsonify({
        'datas': [{
            'url': url_for('api.get_data', id=data.data_id),
            'patient': url_for('api.get_patient', id=patient.patient_id),
            'sn': data.sn,
            'id_number': data.id_number,
            'time': str(data.time),
            'date': str(data.date),
            'glucose': data.glucose
        }],
        'status': 'success',
        'reason': 'the data has been deleted'
    }), 200


"""

@api {DELETE} /api/v1.0/datas/<int:id> 删除id所代表的数据的信息
@apiGroup datas
@apiName 删除id所代表的数据的信息

@apiParam (params) {String} id 数据id 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回删除的数据的信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        'datas':[{
            'url': url_for('api.get_data', id=data.data_id),
            'patient': url_for('api.get_patient', id=patient.patient_id),
            'sn': data.sn,
            'id_number': data.id_number,
            'time': str(data.time),
            'date': str(data.date),
            'glucose': data.glucose
        }],
        'status':'success',
        'reason':'the data has been deleted'
    }
    非主治医师删除
    {   
        'status':'fail',
        'reason':'no root'
    }

"""