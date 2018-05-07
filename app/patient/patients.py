from app.patient import patient_blueprint
from app import db
from flask import request, jsonify, url_for, current_app
from app.models import Patient, Data, Bed
from sqlalchemy.exc import OperationalError
from flask_login import login_required
import json
from app.form_model import PatientValidation, GetPatientValidation, ChangePatientValidation, PatientDataValidation, PatientHistoryValidation
from marshmallow.exceptions import ValidationError

def std_json(d):
    r = {}
    for k, v in d.items():
        r[k] = json.loads(v)
    return r

@patient_blueprint.route('/patients', methods = ['POST'])
@login_required
def new_patient():
    params_dict = {
        'patient_id': request.json.get('patient_id', None),
        'doctor_name': request.json.get('doctor_name', None),
        'id_number': request.json.get('id_number', None),
        'tel': request.json.get('tel', None),
        'age': request.json.get('age', None),
        'sex': request.json.get('sex', None),
        'patient_name': request.json.get('patient_name', None)
    }
    try:
        PatientValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    id_number = request.json['id_number']
    bed_id = request.json['bed_id']
    patient = Patient.query.filter(Patient.id_number == id_number).first()
    if patient:
        return jsonify({
            'status': 'fail',
            'reason': 'the id_number has been used'
        })
    patient = Patient.from_json(request.json)
    bed = Bed.query.filter(Bed.bed_id==bed_id).first()
    try:
        db.session.add(patient)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':patient.to_json()
        })
    bed.id_number = id_number
    try:
        db.session.add(bed)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':bed.to_json()
        })
    return jsonify({
        'patients':[patient.to_json()],
        'status':'success',
        'reason':'the data has been added'
    })


"""
@api {POST} /patients 新建病人信息(json数据)
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


@patient_blueprint.route('/patients')
@login_required
def get_patients():
    params_dict = {
        'patient_id': request.args.get('patient_id', None, type=int),
        'doctor_name': request.args.get('doctor_name', None, type=str),
        'id_number': request.args.get('id_number', None, type=str),
        'tel': request.args.get('tel', None, type=str),
        'age': request.args.get('age', None, type=int),
        'sex': request.args.get('sex', None, type=str),
        'patient_name': request.args.get('patient_name', None, type=str),
        'limit': request.args.get('limit', None, type=int),
        'per_page': request.args.get('per_page', None, type=int)
    }
    try:
        GetPatientValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    page = request.args.get('page', 1, type=int)
    fields = [i for i in Patient.__table__.c._data]
    patients = Patient.query
    limit = None
    per_page = current_app.config['PATIENTS_PRE_PAGE']
    for k, v in std_json(request.args).items():
        if k in fields:
            patients = patients.filter_by(**{k: v})
        if k == 'per_page':
            per_page = v
        if k == 'limit':
            limit = v
    patients = patients.limit(limit).from_self() if limit is not None else patients.from_self()
    pagination = patients.paginate(page, per_page=per_page, error_out=False)
    patients = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('patient_blueprint.get_patients', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('patient_blueprint.get_patients', page=page + 1)
    return jsonify({
        'patients': [patient.to_json() for patient in patients],
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
@api {GET} /patients 获取所有病人数据信息(地址栏筛选)
@apiGroup patients
@apiName 获取所有病人数据

@apiParam (params) {String} id_number 医保卡号
@apiParam (params) {String} tel 病人电话号码
@apiParam (params) {Number} doctor_id 医生号码
@apiParam (params) {String} sex 患者性别
@apiParam (params) {Number} limit 查询总数量
@apiParam (params) {Number} per_page 每一页的数量
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
    没有数据
    {
        "status":"fail",
        "reason":"there is no data"
    }
"""


@patient_blueprint.route('/patients/<int:id>', methods = ['PUT'])
@login_required
def change_patient(id):
    params_dict = {
        'patient_id': request.json.get('patient_id', None),
        'doctor_name': request.json.get('doctor_name', None),
        'id_number': request.json.get('id_number', None),
        'tel': request.json.get('tel', None),
        'age': request.json.get('age', None),
        'sex': request.json.get('sex', None),
        'patient_name': request.json.get('patient_name', None)
    }
    try:
        ChangePatientValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    patient = Patient.query.get_or_404(id)
    if 'id_number' in request.json:
        id_number = request.json['id_number']
        may_patient = Patient.query.filter(Patient.id_number == id_number).first()
        if may_patient and patient.id_number != id_number:
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
@api {PUT} /patients/<int:id> 修改id代表的病人信息(json数据)
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


@patient_blueprint.route('/patients/<int:id>')
@login_required
def get_patient(id):
    patient = Patient.query.get_or_404(id)
    return jsonify({
        'patients': [patient.to_json()],
        'status': 'success',
        'reason': 'there is the data'
    })

"""
@api {GET} /patients/<int:id> 根据id获取病人信息
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


@patient_blueprint.route('/patients/<int:id>', methods = ['DELETE'])
@login_required
def delete_patients(id):
    patient = Patient.query.get_or_404(id)
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
@api {DELETE} /patients/<int:id> 删除id所代表的病人信息
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


@patient_blueprint.route('/patients/getfromid')
@login_required
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
@api {GET} /patients/getfromid 根据医疗卡号获取病人信息
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


@patient_blueprint.route('/patients/<int:id>/datas')
@login_required
def get_patient_datas(id):
    params_dict = {
        'data_id': request.args.get('data_id', None, type=int),
        'sn': request.args.get('sn', None, type=str),
        'id_number': request.args.get('id_number', None, type=str),
        'time': request.args.get('time', None, type=str),
        'date': request.args.get('date', None, type=str),
        'glucose': request.args.get('glucose', None, type=float),
        'hidden': request.args.get('hidden', None, type=bool),
        'limit': request.args.get('limit', None, type=int),
        'per_page': request.args.get('per_page', None, type=int)
    }
    try:
        PatientDataValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    patient = Patient.query.get_or_404(id)
    fields = [i for i in Data.__table__.c._data]
    datas = patient.datas
    limit = None
    per_page = current_app.config['PATIENTS_PRE_PAGE']
    for k, v in std_json(request.args).items():
        if k in fields:
            datas = datas.filter(getattr(Data, k) == v)
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
        prev = url_for('patient_blueprint.get_patient_datas', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('patient_blueprint.get_patient_datas', page=page + 1)
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
        'reason': 'there are datas'
    })

"""
@api {GET} /patients/<int:id>/datas 获取id所代表的病人的数据
@apiGroup patients
@apiName 获取id所代表的病人的数据

@apiParam (params) {Number} id 病人id 
@apiParam (Login) {String} login 登录才可以访问
@apiParam (params) {Number} limit 查询总数量
@apiParam (params) {Number} per_page 每一页的数量

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
        'has_prev':'是否有上一页',
        'has_next':'是否有下一页',
        'total': '查询总数量',
        'pages': '查询总页数',
        'per_page': '每一页的数量',
        'status': 'success',
        'reason': 'there are datas'
    }
    @apiError (Error 4xx) 404 对应id的病人不存在

    @apiErrorExample Error-Resopnse:
    HTTP/1.1 404 对应的病人信息不存在 
"""


@patient_blueprint.route('/patients/history')
@login_required
def patients_history():
    params_dict = {
        'patient_id': request.args.get('patient_id', None, type=int),
        'doctor_name': request.args.get('doctor_name', None, type=str),
        'id_number': request.args.get('id_number', None, type=str),
        'tel': request.args.get('tel', None, type=str),
        'age': request.args.get('age', None, type=int),
        'sex': request.args.get('sex', None, type=str),
        'patient_name': request.args.get('patient_name', None, type=str),
        'limit': request.args.get('limit', None, type=int),
        'per_page': request.args.get('per_page', None, type=int),
        'sn': request.args.get('sn', None, type=str),
        'time': request.args.get('time', None, type=str),
        'date': request.args.get('date', None, type=str),
        'glucose': request.args.get('glucose', None, type=float),
        'data_id': request.args.get('data_id', None, type=int),
        'hidden': request.args.get('hidden', None, type=bool),
        'min_age': request.args.get('min_age', None, type=int),
        'max_age': request.args.get('max_age', None, type=int),
        'max_glucose': request.args.get('max_glucose', None, type=float),
        'min_glucose': request.args.get('min_glucose', None, type=float),
        'begin_time': request.args.get('begin_time', None, type=str),
        'end_time': request.args.get('end_time', None, type=str),
        'begin_date': request.args.get('begin_date', None, type=str),
        'end_date': request.args.get('end_date', None, type=str)
    }
    try:
        PatientHistoryValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    datas = Data.query.join(Patient, Patient.id_number == Data.id_number)
    patient_field = [i for i in Patient.__table__.c._data]
    limit = None
    data_field = [i for i in Data.__table__.c._data]
    per_page = current_app.config['PATIENTS_PRE_PAGE']
    for k, v in request.args.items():
        if k in patient_field:
            if hasattr(Patient, k):
                field = getattr(Patient, k)
                datas = datas.filter(field == v)
        if k in data_field:
            if hasattr(Data, k):
                field = getattr(Data, k)
                datas = datas.filter(field == v)
        if k == 'per_page':
            per_page = v
        if k == 'limit':
            limit = v
    max_age = request.args.get('max_age')
    min_age = request.args.get('min_age')
    max_glucose = request.args.get('max_glucose')
    min_glucose = request.args.get('min_glucose')
    begin_time = request.args.get('begin_time')
    begin_time1 = str(begin_time)[0:6]+'00'
    end_time = request.args.get('end_time')
    end_time1 = str(end_time)[0:6]+'59'
    begin_date = request.args.get('begin_date')
    end_date = request.args.get('end_date')
    if max_age:
        datas = datas.filter(Patient.age <= max_age)
    if min_age:
        datas = datas.filter(Patient.age >= min_age)
    if max_glucose:
        datas = datas.filter(Data.glucose <= max_glucose)
    if min_glucose:
        datas = datas.filter(Data.glucose >= min_glucose)
    if begin_time:
        datas = datas.filter(Data.time >= begin_time1)
    if end_time:
        datas = datas.filter(Data.time <= end_time1)
    if end_date:
        datas = datas.filter(Data.date <= end_date)
    if begin_date:
        datas = datas.filter(Data.date >= begin_date)
    print(datas.count())
    datas = datas.order_by(Data.date.desc(), Data.time.desc())
    datas = datas.limit(limit).from_self() if limit is not None else datas.from_self()
    page = request.args.get('page', 1, type=int)
    pagination = datas.paginate(page, per_page=per_page, error_out=False)
    datas = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('patient_blueprint.patients_history', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('patient_blueprint.patients_history', page=page + 1)
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
        'reason': 'there are datas'
    })

"""
@api {GET} /patients/history 获取病人历史信息(浏览器栏筛选)
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
            "time":"数据时间",
            "sex":"患者性别",
            "tel":"患者电话"
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

