from app.data import data_blueprint
from app import db
from flask import request, jsonify, url_for, current_app
from app.models import Patient, Data, Accuchek, SpareData
from sqlalchemy.exc import IntegrityError
from flask_login import login_required
from app.models import InvalidUsage
import json
from app.form_model import DataValidation, DataArtificialValidation, GetDataValidation, GetSpareDataValidation, ChangeSpareDataValidation, ChangeDataValidation
from marshmallow.exceptions import ValidationError
from datetime import datetime
def std_json(d):
    r = {}
    for k, v in d.items():
        try:
            r[k] = json.loads(v)
        except:
            r[k] = v
    return r

sn_numbers = ['00000000', '11111111']
@login_required
@data_blueprint.route('/datas/auto', methods=['POST'])
def new_data_auto():
    params_dict = {
        'data_id': request.json.get('data_id', None),
        'sn': request.json.get('sn', None),
        'patient_id': request.json.get('patient_id',None),
        'glucose': request.json.get('glucose', None),
        'id_number': request.json.get('id_number', None),
        'time': request.json.get('time', None),
        'date': request.json.get('date', None),
        'hidden': request.json.get('hidden', None)
    }
    try:
        DataValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    if request.json['sn'] not in sn_numbers:
        data = Data()
        for k in request.json:
            if hasattr(data, k):
                setattr(data, k, request.json[k])
        if 'date' not in request.json:
            data.date = datetime.utcnow().date()
        if 'time' not in request.json:
            data.time = datetime.utcnow().time()
        accuchek = Accuchek.query.filter(Accuchek.sn == request.json['sn']).first()
        if accuchek is None:
            return jsonify({
                'status':'fail',
                'reason':'血糖仪不存在'
            })
        bed = accuchek.bed if accuchek is not None else None
        patient = bed.patient if bed is not None else None
        id_number = patient.id_number if patient is not None else None
        patient_id = patient.patient_id if patient is not None else None
        data.id_number = id_number
        data.patient_id = patient_id
        try:
            db.session.add(data)
            db.session.commit()
        except IntegrityError as e:
            raise InvalidUsage(message=str(e), status_code=500)
        return jsonify({
            'patient':data.patient.to_json_patient(),
            'data': data.to_json_without_patient(),
            'status': 'success',
            'reason': '数据已经被添加了'
        })
    else:
        data = SpareData()
        for k in request.json:
            if hasattr(data, k):
                setattr(data, k, request.json[k])

        if 'date' not in request.json:
            data.date = datetime.utcnow().date()
        if 'time' not in request.json:
            data.time = datetime.utcnow().time()
        try:
            db.session.add(data)
            db.session.commit()
        except IntegrityError as e:
            raise InvalidUsage(message=str(e), status_code=500)
        return jsonify({
            'data': data.to_full_json(),
            'status': 'success',
            'reason': '数据已经被添加了'
        })



"""
@api {POST} /datas/auto 添加数据(不用手动输入病人数据)(json数据)
@apiGroup datas

@apiParam (params) {String} sn 血糖仪sn码 
@apiParam (params) {Int} patient_id 患者id
@apiParam (params) {String} id_number 患者医疗卡号
@apiParam (params) {Date} date 数据日期_日期格式(0000-00-00)
@apiParam (params) {Time} time 数据时间_时间格式(00:00:00)
@apiParam (params) {Bool} hidden 是否隐藏
@apiParam (params) {Float} glucose 血糖值
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回新添加的数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "data":{
            "patient_name":"患者姓名",
            "age":"患者年龄",
            "tel":"患者电话",
            "date":"数据添加日期",
            "time":"数据添加时间",
            "id_number":"医疗卡号",
            "doctor_name":"医生姓名",
            "sn":"血糖仪sn码",
            "data_id":"数据id",
            "glucose":"血糖值"
        },
        "status":"success",
        "reason":"the data has been added"
    } 
    HTTP/1.1 200 OK
    {
        "data":{
            'data_id':"数据id",
            'sn':"血糖仪sn码",
            'id_number':"患者医疗卡号",
            'time':"数据时间",
            'patient_id':"患者id",
            'date':"数据日期",
            'glucose':"血糖值"
        },
        "patient":{
            'patient_id': "病人id",
            'patient_name':"病人姓名",
            'sex':"病人性别",
            'tel':"病人电话",
            'age':"病人年龄",
            'doctor_name':"医生姓名",
            'id_number':"病人医疗卡号"
        },
        "status":"success",
        "reason":"the data has been added"
    } 
"""


@data_blueprint.route('/datas/artificial', methods=['POST'])
@login_required
def new_data_artificial():
    params_dict = {
        'data_id': request.json.get('data_id', None),
        'sn': request.json.get('sn', None),
        'glucose': request.json.get('glucose', None),
        'id_number': request.json.get('id_number', None),
        'time': request.json.get('time', None),
        'date': request.json.get('date', None),
        'hidden': request.json.get('hidden', None),
        'patient_id': request.json.get('patient_id', None),
        'patient_name': request.json.get('patient_name', None),
        'sex': request.json.get('sex', None),
        'tel': request.json.get('tel', None),
        'age': request.json.get('age', None),
        'doctor_name': request.json.get('doctor_name', None)
    }
    try:
        DataArtificialValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    accuchek = Accuchek.query.filter(Accuchek.sn == request.json.get('sn')).first()
    if accuchek is None:
        return jsonify({
            'status': 'fail',
            'reason': '血糖仪不存在'
        })
    data = Data()
    for k in request.json:
        if hasattr(data, k):
            setattr(data, k, request.json[k])

    if 'date' not in request.json:
        data.date = datetime.utcnow().date()
    if 'time' not in request.json:
        data.time = datetime.utcnow().time()
    patient_id = request.json['patient_id']
    patient = Patient.query.filter(Patient.patient_id == patient_id).first()
    if patient is None:
        patient = Patient()
    for k in request.json:
        if hasattr(patient, k):
            setattr(patient, k, request.json[k])
    try:
        db.session.add(patient)
        db.session.commit()
    except IntegrityError as e:
        raise InvalidUsage(message=str(e), status_code=500)
    try:
        db.session.add(data)
        db.session.commit()
    except IntegrityError as e:
        raise InvalidUsage(message=str(e), status_code=500)
    return jsonify({
        'data': data.to_json_without_patient(),
        'status': 'success',
        'reason': '数据已经被添加了'
    })


"""
@api {POST} /datas/artificial 添加数据(不用手动输入病人数据)(json数据)
@apiGroup datas

@apiParam (json) {String} id_number 医疗卡号
@apiParam (json) {String} patient_name 病人姓名
@apiParam (json) {Int} patient_id 患者id
@apiParam (json) {String} sex 病人性别
@apiParam (json) {Int} patient_id 患者id
@apiParam (json) {String} tel 病人电话
@apiParam (json) {Int} age 病人年龄
@apiParam (json) {String} doctor_name 医生姓名
@apiParam (json) {String} sn 血糖仪sn码 
@apiParam (json) {Date} date 数据日期_日期格式(0000-00-00)
@apiParam (json) {Time} time 数据时间_时间格式(00:00:00)
@apiParam (json) {Float} glucose 血糖值
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回新添加的数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "datas":[{
            'data_id':"数据id",
            "patient":{
                'patient_id': "病人id",
                'patient_name':"病人姓名",
                'sex':"病人性别",
                'tel':"病人电话",
                'age':"病人年龄",
                'doctor_name':"医生姓名",
                'id_number':"病人医疗卡号",
                'datas':"病人数据地址"
            },
            'sn':"血糖仪sn码",
            'id_number':"患者医疗卡号",
            'time':"数据时间",
            'date':"数据日期",
            'glucose':"血糖值"
        }],
        "status":"success",
        "reason":"the data has been added"
    }  
"""


@data_blueprint.route('/datas')
@login_required
def get_datas():
    params_dict = {
        'data_id': request.args.get('data_id', None, type=int),
        'patient_id': request.args.get('patient_id', None, type=int),
        'sn': request.args.get('sn', None, type=str),
        'glucose': request.args.get('glucose', None, type=float),
        'id_number': request.args.get('id_number', None, type=str),
        'time': request.args.get('time', None, type=str),
        'date': request.args.get('date', None, type=str),
        'hidden': request.args.get('hidden', None, type=bool),
        'limit': request.args.get('limit', None, type=int),
        'per_page': request.args.get('per_page', None, type=int)
    }
    try:
        GetDataValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    data_fields = [i for i in Data.__table__.c._data]
    fields = data_fields
    datas = Data.query.order_by(Data.date.desc(), Data.time.desc())
    per_page = current_app.config['PATIENTS_PRE_PAGE']
    limit = None
    for k, v in std_json(request.args).items():
        if k in fields:
            datas = datas.filter_by(**{k: v})
        if k == 'per_page':
            per_page = v
        if k == 'limit':
            limit = v
    datas = datas.limit(limit).from_self() if limit is not None else datas.from_self()
    page = request.args.get('page', 1, type=int)
    pagination = datas.paginate(page, per_page=per_page, error_out=False)
    datas = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('data_blueprint.get_datas', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('data_blueprint.get_datas', page=page + 1)
    return jsonify({
        'datas': [data.to_json() for data in datas],
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
@api {GET} /datas 获取所有数据信息
@apiGroup datas

@apiParam (params) {String} sn 血糖仪sn码 
@apiParam (params) {Int} limit 查询总数量
@apiParam (params) {Int} patient_id 患者id
@apiParam (params) {Int} per_page 每一页的数量
@apiParam (params) {Date} date 数据日期_日期格式(0000-00-00)
@apiParam (params) {Time} time 数据时间_时间格式(00:00:00)
@apiParam (params) {Float} glucose 血糖值
@apiParam (params) {Int} data_id 数据id
@apiParam (params) {String} id_number 医疗卡号
@apiParam (params) {Bool} hidden 是否隐藏
@apiParam (Login) {String} login 登录才可以访问


@apiSuccess {Array} datas 返回查询到的数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "datas":[{
            "date":"数据添加日期",
            "time":"数据添加时间",
            "id_number":"医疗卡号",
            "patient":{
                'patient_id': "病人id",
                'patient_name':"病人姓名",
                'sex':"病人性别",
                'tel':"病人电话",
                'age':"病人年龄",
                'doctor_name':"医生姓名",
                'id_number':"病人医疗卡号",
                'datas':"病人数据地址"
            },
            "sn":"血糖仪sn码",,
            "glucose":"血糖值",
            "data_id":"数据id"
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

@data_blueprint.route('/sparedatas')
@login_required
def get_datas_sparedata():
    params_dict = {
        'data_id': request.args.get('data_id', None, type=int),
        'sn': request.args.get('sn', None, type=str),
        'glucose': request.args.get('glucose', None, type=float),
        'id_number': request.args.get('id_number', None, type=str),
        'patient_name': request.args.get('patient_name', None, type=str),
        'sex': request.args.get('sex', None, type=str),
        'tel': request.args.get('tel', None, type=str),
        'age': request.args.get('age', None, type=int),
        'doctor_name': request.args.get('doctor_name', None, type=str),
        'time': request.args.get('time', None, type=str),
        'date': request.args.get('date', None, type=str),
        'hidden': request.args.get('hidden', None, type=bool),
        'limit': request.args.get('limit', None, type=int),
        'per_page': request.args.get('per_page', None, type=int)
    }
    try:
        GetSpareDataValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    if 'sn' not in request.args:
        return jsonify({
            'status':'fail',
            'reason':'请求中没有血糖仪sn码'
        })
    fields = [i for i in SpareData.__table__.c._data]
    per_page = current_app.config['PATIENTS_PRE_PAGE']
    limit = None
    datas = SpareData.query.order_by(SpareData.date.desc(), SpareData.time.desc())
    for k, v in std_json(request.args).items():
        if k in fields:
            datas = datas.filter_by(**{k: v})
        if k == 'per_page':
            per_page = v
        if k == 'limit':
            limit = v
    datas = datas.limit(limit).from_self() if limit is not None else datas.from_self()
    page = request.args.get('page', 1, type=int)
    pagination = datas.paginate(page, per_page=per_page, error_out=False)
    datas = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('data_blueprint.get_datas_sparedata', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('data_blueprint.get_datas_sparedata', page=page + 1)
    return jsonify({
        'datas': [data.to_full_json() for data in datas],
        'prev': prev,
        'next': next,
        'has_prev':pagination.has_prev,
        'has_next':pagination.has_next,
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'status': 'success',
        'reason': '这里是查询到的备用机数据'
    })
"""
@api {GET} /sparedatas 获取备用机数据
@apiGroup datas

@apiParam (params) {String} sn 血糖仪sn码 
@apiParam (params) {Int} data_id 数据id
@apiParam (params) {String} patient_name 患者姓名
@apiParam (params) {String} sex 患者性别
@apiParam (params) {String} tel 患者电话
@apiParam (params) {String} doctor_name 医生姓名
@apiParam (params) {Int} age 患者年龄
@apiParam (params) {String} id_number 医疗卡号 
@apiParam (params) {Bool} hidden 是否隐藏 
@apiParam (params) {Int} limit 查询总数量
@apiParam (params) {Int} per_page 每一页的数量
@apiParam (params) {Date} date 数据日期_日期格式(0000-00-00)
@apiParam (params) {Time} time 数据时间_时间格式(00:00:00)
@apiParam (params) {Float} glucose 血糖值
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回查询到的数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "datas":[{
            "data_id":"备用机数据号",
            "patient_name":"患者姓名",
            "age":"患者年龄",
            "tel":"患者电话",
            "date":"数据添加日期",
            "time":"数据添加时间",
            "id_number":"医疗卡号",
            "patient":"病人地址",
            "sn":"血糖仪sn码",
            "data_id":"数据id",
            "glucose":"血糖值"
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


@data_blueprint.route('/datas/<int:id>')
@login_required
def get_data(id):
    data = Data.query.get_or_404(id)
    return jsonify({
        'data': data.to_json(),
        'status': 'success',
        'reason': '这里是查询到的数据'
    })


"""
@api {GET} /datas/<int:id> 根据id获取数据信息
@apiGroup datas

@apiParam (params) {Int} id 数据id 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回id所代表数据信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "data":{
            "date":"数据添加日期",
            "time":"数据添加时间",
            "id_number":"医疗卡号",
            "patient":{
                'patient_id': "病人id",
                'patient_name':"病人姓名",
                'sex':"病人性别",
                'tel':"病人电话",
                'age':"病人年龄",
                'doctor_name':"医生姓名",
                'id_number':"病人医疗卡号",
                'datas':"病人数据地址"
            },
            "sn":"血糖仪sn码",
            "data_id":"数据id"
        },
        "status":"success",
        "reason":"there is the data"
    }

"""

@data_blueprint.route('/sparedatas/<int:id>', methods=['PUT'])
@login_required
def change_sparedata_data(id):
    params_dict = {
        'data_id': request.json.get('data_id', None),
        'sn': request.json.get('sn', None),
        'glucose': request.json.get('glucose', None),
        'id_number': request.json.get('id_number', None),
        'time': request.json.get('time', None),
        'date': request.json.get('date', None),
        'hidden': request.json.get('hidden', None),
        'doctor_name': request.json.get('doctor_name', None),
        'sex': request.json.get('sex', None),
        'patient_name': request.json.get('patient_name', None),
        'age': request.json.get('age', None),
        'tel': request.json.get('tel', None)
    }

    try:
        ChangeSpareDataValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    data = SpareData.query.get_or_404(id)
    for k in request.json:
        if hasattr(data, k):
            setattr(data, k, request.json[k])
    try:
        db.session.add(data)
        db.session.commit()
    except IntegrityError as e:
        raise InvalidUsage(message=str(e), status_code=500)
    return jsonify({
        'sparedata':data.to_full_json(),
        'status':'success',
        'reason':'备用机数据已经被修改了'
    })

"""
@api {PUT} /sparedatas/<int:id> 根据id修改备用机数据
@apiGroup datas

@apiParam (params) {Int} id 备用机数据id 
@apiParam (json) {String} sn 备用机sn码
@apiParam (json) {String} id_number 患者医疗卡号
@apiParam (json) {Time} time 数据时间
@apiParam (json) {Date} date 数据日期
@apiParam (json) {String} doctor_name 医生姓名
@apiParam (json) {Float} glucose 血糖值
@apiParam (json) {String} sex 患者性别
@apiParam (json) {String} patient_name 患者姓名
@apiParam (json) {Int} age 患者年龄
@apiParam (json) {String} tel 患者电话
@apiParam (json) {Bool} hidden 是否隐藏（0：隐藏， 1：不隐藏）
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回修改后的备用机数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "sparedatas":{
            "data_id":"备用机数据号",
            "patient_name":"患者姓名",
            "age":"患者年龄",
            "tel":"患者电话",
            "date":"数据添加日期",
            "time":"数据添加时间",
            "id_number":"医疗卡号",
            "patient":"病人地址",
            "sn":"血糖仪sn码",
            "data_id":"数据id",
            "glucose":"血糖值"
        },
        "status":"success",
        "reason":"there is the data"
    }
    {
        "status":"fail",
        "reason":""
    }
"""


@data_blueprint.route('/sparedatas/<int:id>', methods=['DELETE'])
@login_required
def delete_sparedata_data(id):
    data = SpareData.query.get_or_404(id)
    try:
        db.session.delete(data)
        db.session.commit()
    except IntegrityError as e:
        raise InvalidUsage(message=str(e), status_code=500)
    return jsonify({
        'status':'success',
        'reason':'备用机数据已经被删除了'
    })

"""
@api {DELTET} /sparedatas/<int:id> 根据id删除备用机数据
@apiGroup datas

@apiParam (params) {String} id 备用机数据id 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回删除状态

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "status":"success",
        "reason":"there is the data"
    }

"""

@data_blueprint.route('/sparedatas/<int:id>')
@login_required
def get_sparedata_data(id):
    data = SpareData.query.filter(SpareData.data_id == id).first()
    return jsonify({
        'status':'success',
        'reason':'这里是被查询的备用机数据',
        'sparedata': data.to_full_json()
    })

"""
@api {GET} /sparedatas/<int:id> 根据id查询备用机数据
@apiGroup datas

@apiParam (params) {String} id 备用机数据id 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回查询到的备用机数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "sparedatas":{
            "data_id":"备用机数据号",
            "patient_name":"患者姓名",
            "age":"患者年龄",
            "tel":"患者电话",
            "date":"数据添加日期",
            "time":"数据添加时间",
            "id_number":"医疗卡号",
            "doctor_name":"医生姓名",
            "sn":"血糖仪sn码",
            "data_id":"数据id",
            "glucose":"血糖值"
        },
        "status":"success",
        "reason":"there is the data"
    }
"""


@data_blueprint.route('/datas/<int:id>', methods=['PUT'])
@login_required
def change_data(id):
    params_dict = {
        'data_id': request.json.get('data_id', None),
        'sn': request.json.get('sn', None),
        'glucose': request.json.get('glucose', None),
        'id_number': request.json.get('id_number', None),
        'time': request.json.get('time', None),
        'date': request.json.get('date', None),
        'patient_id': request.json.get('patient_id', None),
        'hidden': request.json.get('hidden', None)
    }
    try:
        ChangeDataValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    data = Data.query.get_or_404(id)
    for k in request.json:
        if hasattr(data, k):
            setattr(data, k, request.json[k])
    try:
        db.session.add(data)
        db.session.commit()
    except IntegrityError as e:
        return jsonify({
            'status': 'fail',
            'reason': e,
            'data': data.to_json()
        })
    return jsonify({
        'data': data.to_full_json(),
        'status': 'success',
        'reason': '数据已经被修改'
    }), 200


"""
@api {PUT} /datas/<int:id> 更改id所代表的数据的信息
@apiGroup datas

@apiParam (params) {Int} id 数据id
@apiParam (json) {Int} patient_id 患者id
@apiParam (json) {String} id_number 医疗卡号
@apiParam (json) {String} sn 血糖仪sn码 
@apiParam (json) {Date} date 数据日期_日期格式(0000-00-00)
@apiParam (json) {String} time 数据时间_时间格式(00:00:00)
@apiParam (params) {Number} limit 查询总数量
@apiParam (params) {Number} per_page 每一页的数量
@apiParam (json) {Float} glucose 血糖值
@apiParam (json) {Bool} hidden 是否隐藏
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回id所代表数据信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "datas":{
            "date":"数据添加日期",
            "time":"数据添加时间",
            "id_number":"医疗卡号",
            "patient_name":"病人姓名",
            "age":"患者年龄",
            "tel":"患者电话",
            "sn":"血糖仪sn码",
            "data_id":"数据id",
            "glucose":"血糖值",
            "sex":"患者性别",
            "doctor_name":"医生姓名"
        },
        "status":"success",
        "reason":"the data has been changed"
    }
    不是本人主任医生修改
    {
        "status":"fail",
        "reason":"no root"
    }
"""


@data_blueprint.route('/datas/<int:id>', methods=['DELETE'])
@login_required
def delete_data(id):
    data = Data.query.get_or_404(id)
    try:
        db.session.delete(data)
        db.session.commit()
    except IntegrityError as e:
        raise InvalidUsage(message=str(e), status_code=500)
    return jsonify({
        'status': 'success',
        'reason': '数据已经被删除'
    }), 200


"""

@api {DELETE} /datas/<int:id> 删除id所代表的数据的信息
@apiGroup datas

@apiParam (params) {String} id 数据id 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回删除的情况

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        'status':'success',
        'reason':'the data has been deleted'
    }
    操作失败
    {   
        'status':'fail',
        'reason':''
    }

"""