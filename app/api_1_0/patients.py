from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for, current_app
from ..models import Patient, Operator, Data, Bed
from .authentication import auth
from sqlalchemy.exc import OperationalError
from ..decorators import allow_cross_domain
from flask_login import login_required, current_user
@api.route('/patients', methods = ['POST'])
@login_required
@allow_cross_domain
def new_patient():
    id_number = request.json['id_number']
    patient = Patient.query.filter(Patient.id_number == id_number).first()
    if patient:
        return jsonify({
            'status': 'fail',
            'reason': 'the id_number has been used'
        })
    patient = Patient.from_json(request.json)
    try:
        db.session.add(patient)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':patient.to_json()
        })
    return jsonify({
        'patients':[patient.to_json()],
        'status':'success',
        'reason':'the data has been added'
    })


"""
@api {POST} /api/v1.0/patients 新建病人信息(json数据)
@apiGroup patients
@apiName 新建病人信息

@apiParam (params) {String} id_number 医保卡号
@apiParam (params) {String} tel 病人电话号码
@apiParam (params) {Number} doctor_id 医生号码
@apiParam (params) {String} sex 患者性别
@apiParam (params) {String} patient_name 患者姓名
@apiParam (params) {Number} age 患者年龄
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} patients 返回新病人信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "patients":[{
            "url": "病人信息地址",
            "patient_name":"病人姓名",
            "sex":"病人性别",
            "tel":"病人电话",
            "age":"病人年龄",
            "doctor_id":"医生号码",
            "id_number":"医保卡号",
            "datas":"病人数据地址"
        }],
        "status":"success",
        "reason":"the data has been added"
    }
    医保卡号如果被注册过了
    {
        "status":"fail",
        "reason":"the id_number has been used"
    }

"""


@api.route('/patients')
@login_required
@allow_cross_domain
def get_patients():
    page = request.args.get('page', 1, type=int)
    fields = [i for i in Patient.__table__.c._data]
    patients = Patient.query
    for k, v in request.args.items():
        if k in fields:
            patients = patients.filter_by(**{k: v})
    if patients.count()!=0:
        pagination = patients.paginate(page, per_page=current_app.config['PATIENTS_PRE_PAGE'], error_out=False)
        patients = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.get_patients', page = page-1)
        next = None
        if pagination.has_next:
            next = url_for('api.get_patients', page = page+1)
        return jsonify({
            'patients':[patient.to_json() for patient in patients],
            'prev':prev,
            'next':next,
            'count':pagination.total,
            "pages":pagination.pages,
            'status':'success',
            'reason':'there are the datas'
        })
    else:
        return jsonify({
            'status':'fail',
            'reason':'there is no data'
        })

"""
@api {GET} /api/v1.0/patients 获取所有病人数据信息(地址栏筛选)
@apiGroup patients
@apiName 获取所有病人数据

@apiParam (params) {String} id_number 医保卡号
@apiParam (params) {String} tel 病人电话号码
@apiParam (params) {Number} doctor_id 医生号码
@apiParam (params) {String} sex 患者性别
@apiParam (params) {String} patient_name 患者姓名
@apiParam (params) {Number} age 患者年龄
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} patients 返回查询到的病人信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "patients":[{
            "url": "病人信息地址",
            "patient_name":"病人姓名",
            "sex":"病人性别",
            "tel":"病人电话",
            "age":"病人年龄",
            "doctor_id":"医生号码",
            "id_number":"医保卡号",
            "datas":"病人数据地址"    
        }],
        "prev":"上一页",
        "next":"下一页",
        "count":"总数量",
        "pages":"总页数",
        "status":"success",
        "reason":"there are the datas"
    }
    没有数据
    {
        "status":"fail",
        "reason":"there is no data"
    }
"""


@api.route('/patients/<int:id>', methods = ['PUT'])
@login_required
@allow_cross_domain
def change_patient(id):
    patient = Patient.query.get_or_404(id)
    if 'id_number' in request.json:
        id_number = request.json['id_number']
        may_patient = Patient.query.filter(Patient.id_number == id_number).first()
        if may_patient:
            if may_patient.patient_id != patient.patient_id:
                return jsonify({
                    'status':'fail',
                    'reason':'the id_number has been used'
                })
    for k in request.json:
        if hasattr(patient, k):
            setattr(patient, k, request.json[k])
    try:
        db.session.add(patient)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':patient.to_json()
        })
    return jsonify({
        'patients': [patient.to_json()],
        'status': 'success',
        'reason': 'the data has been changed'
    })

"""
@api {PUT} /api/v1.0/patients/<int:id> 修改id代表的病人信息(json数据)
@apiGroup patients
@apiName 修改id代表的病人信息

@apiParam (params) {Number} id 病人id
@apiParam (params) {String} id_number 医保卡号
@apiParam (params) {String} tel 病人电话号码
@apiParam (params) {Number} doctor_id 医生号码
@apiParam (params) {String} sex 患者性别
@apiParam (params) {String} patient_name 患者姓名
@apiParam (params) {Number} age 患者年龄
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} patients 返回修改后的病人信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "patients":[{
            "url": "病人信息地址",
            "patient_name":"病人姓名",
            "sex":"病人性别",
            "tel":"病人电话",
            "age":"病人年龄",
            "doctor_id":"医生号码",
            "id_number":"医保卡号",
            "datas":"病人数据地址"
        }],
        "status":"success",
        "reason":"the data has been changed"
    }
    医保卡号已注册
    {
        "status":"fail",
        "reason":"the id_number has been used"
    }
    @apiError (Error 4xx) 404 对应id的病人不存在

    @apiErrorExample Error-Resopnse:
    HTTP/1.1 404 对应的病人信息不存在   
"""


@api.route('/patients/<int:id>')
@login_required
@allow_cross_domain
def get_patient(id):
    patient = Patient.query.get_or_404(id)
    return jsonify({
        'patients': [patient.to_json()],
        'status': 'success',
        'reason': 'there is the data'
    })

"""
@api {GET} /api/v1.0/patients/<int:id> 根据id获取病人信息
@apiGroup patients
@apiName 根据id获取病人信息

@apiParam (params) {Number} id 病人id 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} patients 返回id所代表的病人信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "patients":[{
            "url": "病人信息地址",
            "patient_name":"病人姓名",
            "sex":"病人性别",
            "tel":"病人电话",
            "age":"病人年龄",
            "doctor_id":"医生号码",
            "id_number":"医保卡号",
            "datas":"病人数据地址"
        }],
        "status":"success",
        "reason":"there is the data"
    }
    @apiError (Error 4xx) 404 对应id的病人不存在

    @apiErrorExample Error-Resopnse:
    HTTP/1.1 404 对应的病人信息不存在   
"""


@api.route('/patients/<int:id>', methods = ['DELETE'])
@login_required
@allow_cross_domain
def delete_patients(id):
    patient = Patient.query.get_or_404(id)
    if current_user.id != patient.doctor_id:
        return jsonify({
            'status':'fail',
            'reason':'no root'
        })
    for data in patient.datas:
        try:
            db.session.delete(data)
            db.session.commit()
        except OperationalError as e:
            return jsonify({
                'status':'fail',
                'reason':e,
                'data':data.to_json()
            })
    try:
        db.session.delete(patient)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'reason': e,
            'data': patient.to_json()
        })
    return jsonify({
        'patients':[patient.to_json()],
        'status':'success',
        'reason':'the data has been deleted'
    })

"""
@api {DELETE} /api/v1.0/patients/<int:id> 删除id所代表的病人信息
@apiGroup patients
@apiName 删除id所代表的病人信息

@apiParam (params) {Number} id 病人id 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} patients 返回删除后的病人信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "patients":[{
            "url": "病人信息地址",
            "patient_name":"病人姓名",
            "sex":"病人性别",
            "tel":"病人电话",
            "age":"病人年龄",
            "doctor_id":"医生号码",
            "id_number":"医保卡号",
            "datas":"病人数据地址"
        }],
        "status":"success",
        "reason":"the data has been deleted"
    }
    @apiError (Error 4xx) 404 对应id的病人不存在

    @apiErrorExample Error-Resopnse:
    HTTP/1.1 404 对应的病人信息不存在   
"""


@api.route('/patients/get-from-id')
@login_required
@allow_cross_domain
def get_from_id():
    id_number = request.args.get('id_number')
    patient = Patient.query.filter(Patient.id_number == id_number).first()
    if patient:
        return jsonify({
            'patients': [patient.to_json()],
            'status': 'success',
            'reason': 'there is the data'
        })
    else:
        return jsonify({
            'status':'fail',
            'reason':'the patient does not exist'
        })

"""
@api {GET} /api/v1.0/patients/get-from-id 根据医疗卡号获取病人信息
@apiGroup patients
@apiName 根据医疗卡号获取病人信息

@apiParam (params) {String} id_number 医疗卡号 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} patients 返回根据医疗卡号获取的病人信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "patients":[{
            "url": "病人信息地址",
            "patient_name":"病人姓名",
            "sex":"病人性别",
            "tel":"病人电话",
            "age":"病人年龄",
            "doctor_id":"医生号码",
            "id_number":"医保卡号",
            "datas":"病人数据地址"
        }],
        "status":"success",
        "reason":"there is the data"
    }
    这个医疗卡号没有注册过
    {
        "status":"fail",
        "reason":"the patient does not exist"
    }  
"""


@api.route('/patients/<int:id>/datas')
@login_required
@allow_cross_domain
def get_patient_datas(id):
    patient = Patient.query.get_or_404(id)
    datas = patient.datas
    if datas.count()!=0:
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
@api {GET} /api/v1.0/patients/<int:id>/datas 获取id所代表的病人的数据
@apiGroup patients
@apiName 获取id所代表的病人的数据

@apiParam (params) {Number} id 病人id 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回id所表示病人的数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "datas":[{
            "date":"数据日期",
            "glucose":"血糖值",
            "id_number":"医疗卡号",
            "patient":"病人地址",
            "sn":"血糖仪sn码",
            "url":"数据地址",
            "time":"数据时间"
        }]，
        "prev":"上一页地址",
        "next":"下一页地址",
        "count":"总数量",
        "pages":"总页数",
        "status":"success",
        "reason":"there are the datas"    
    }
    没有数据
    {
        "status":"fail",
        "reason":"there is no data"
    }
    @apiError (Error 4xx) 404 对应id的病人不存在

    @apiErrorExample Error-Resopnse:
    HTTP/1.1 404 对应的病人信息不存在 
"""


@api.route('/patients/history')
@login_required
@allow_cross_domain
def patients_history():
    datas = Data.query.join(Patient, Patient.id_number == Data.id_number)
    patient_name = request.args.get('patient_name')
    sex = request.args.get('sex')
    age = request.args.get('age')
    tel = request.args.get('tel')
    id_number = request.args.get('id_number')
    max_age = request.args.get('max_age')
    min_age = request.args.get('min_age')
    max_glucose = request.args.get('max_glucose')
    min_glucose = request.args.get('min_glucose')
    begin_time = request.args.get('begin_time')
    end_time = request.args.get('end_time')
    begin_date = request.args.get('begin_date')
    end_date = request.args.get('end_date')
    if patient_name:
        datas = datas.filter(Patient.patient_name == patient_name)
    if sex:
        datas = datas.filter(Patient.sex == sex)
    if age:
        datas = datas.filter(Patient.age == age)
    if tel:
        datas = datas.filter(Patient.tel == tel)
    if id_number:
        datas = datas.filter(Patient.id_number == id_number)
    if max_age:
        datas = datas.filter(Patient.age <= max_age)
    if min_age:
        datas = datas.filter(Patient.age >= min_age)
    if max_glucose:
        datas = datas.filter(Data.glucose <= max_glucose)
    if min_glucose:
        datas = datas.filter(Data.glucose >= min_glucose)
    if begin_time:
        datas = datas.filter(Data.time >= begin_time)
    if end_time:
        datas = datas.filter(Data.time <= end_time)
    if end_date:
        datas = datas.filter(Data.date <= end_date)
    if begin_date:
        datas = datas.filter(Data.date >= begin_date)
    if datas.count()!=0:
        page = request.args.get('page', 1, type=int)
        pagination = datas.paginate(page, per_page=current_app.config['PATIENTS_PRE_PAGE'], error_out=False)
        datas = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.patients_history', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('api.patients_history', page=page + 1)
        return jsonify({
            'datas': [data.to_json() for data in datas],
            'prev': prev,
            'next': next,
            'count': pagination.total,
            'pages':pagination.pages,
            'status':'success',
            'reason':'there are the datas'
        })
    else:
        return jsonify({
            'status':'fail',
            'reason':'there is no data'
        })

"""
@api {GET} /api/v1.0/patients/history 获取病人历史信息(浏览器栏筛选)
@apiGroup patients
@apiName 获取id所代表的病人的数据

@apiParam (params) {String} id_number 医疗卡号 
@apiParam (params) {String} patient_name 病人名字
@apiParam (params) {String} sex 病人性别
@apiParam (params) {String} tel 病人电话
@apiParam (params) {Number} age 病人年龄
@apiParam (params) {Number} max_age 病人最大年龄
@apiParam (params) {Number} min_age 病人最小年龄
@apiParam (params) {Number} max_glucose 病人最大血糖值
@apiParam (params) {Number} min_glucose 病人最小血糖值
@apiParam (params) {String} begin_time 开始时间_时间格式（00:00:00）
@apiParam (params) {String} end_time 结束时间 
@apiParam (params) {String} begin_date 开始日期_日期格式（0000-00-00）
@apiParam (params) {String} end_date
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回筛选过的数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "datas":[{
            "date":"数据日期",
            "glucose":"血糖值",
            "id_number":"医疗卡号",
            "patient":"病人地址",
            "sn":"血糖仪sn码",
            "url":"数据地址",
            "time":"数据时间"
        }],
        "prev":"上一页地址",
        "next":"下一页地址",
        "count":"总数量",
        "pages":"总页数",
        "status":"success",
        "reason":"there are the datas"    
    }
    没有数据
    {
        "status":"fail",
        "reason":"there is no data"
    } 
"""

