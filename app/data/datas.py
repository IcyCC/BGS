from app.data import data
from app import db
from flask import request, jsonify, url_for, current_app
from app.models import Patient, Data, Accuchek, GuargData
from sqlalchemy.exc import OperationalError
from flask_login import login_required

sn_numbers = ['00000000', '11111111']
@login_required
@data.route('/datas/auto', methods=['POST'])
def new_data_auto():
    if request.json['sn'] not in sn_numbers:
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
    else:
        data = GuargData()
        for k in request.json:
            if hasattr(data, k):
                setattr(data, k, request.json[k])
        try:
            db.session.add(data)
            db.session.commit()
        except OperationalError as e:
            return jsonify({
                'status': 'fail',
                'reason': str(e)
            })
        return jsonify({
            'datas': [data.to_full_json()],
            'status': 'success',
            'reason': 'the data has been added'
        })



"""
@api {POST} /data/datas/auto 添加数据(不用手动输入病人数据)(json数据)
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
            "patient_name":"患者姓名",
            "age":"患者年龄",
            "tel":"患者电话",
            "date":"数据添加日期",
            "time":"数据添加时间",
            "id_number":"医疗卡号",
            "patient":"病人地址",
            "sn":"血糖仪sn码",
            "url":"数据地址",
            "glucose":"血糖值"
        }],
        "status":"success",
        "reason":"the data has been added"
    } 
"""


@data.route('/datas/artificial', methods=['POST'])
@login_required
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
@api {POST} /data/datas/artificial 添加数据(不用手动输入病人数据)(json数据)
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


@data.route('/datas')
@login_required
def get_datas():
    data_fields = [i for i in Data.__table__.c._data]
    fields = data_fields
    datas = Data.query
    for k, v in request.args.items():
        if k in fields:
            datas = datas.filter_by(**{k: v})
    datas = datas.order_by(Data.date.desc(), Data.time.desc()).filter(Data.hidden == 0)
    if datas.count() != 0:
        page = request.args.get('page', 1, type=int)
        pagination = datas.paginate(page, per_page=current_app.config['PATIENTS_PRE_PAGE'], error_out=False)
        datas = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('data.get_datas', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('data.get_datas', page=page + 1)
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
@api {GET} /data/datas 获取所有数据信息
@apiGroup datas
@apiName 获取所有数据信息

@apiParam (params) {String} sn 血糖仪sn码 
@apiParam (params) {String} date 数据日期_日期格式(0000-00-00)
@apiParam (params) {String} time 数据时间_时间格式(00:00:00)
@apiParam (params) {Number} glucose 血糖值
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回查询到的数据

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

@data.route('/guard')
@login_required
def get_datas_guard():
    if 'sn' in request.args:
        sn = request.args['sn']
    else:
        return jsonify({
            'status':'fail',
            'reason':'no sn in request'
        })
    data_fields = [i for i in GuargData.__table__.c._data]
    fields = data_fields
    datas = GuargData.query
    for k, v in request.args.items():
        if k in fields:
            datas = datas.filter_by(**{k: v})
    datas = datas.order_by(GuargData.date.desc(), GuargData.time.desc()).filter(GuargData.hidden == 0).filter(GuargData.sn == sn)
    if datas.count() != 0:
        page = request.args.get('page', 1, type=int)
        pagination = datas.paginate(page, per_page=current_app.config['PATIENTS_PRE_PAGE'], error_out=False)
        datas = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('data.get_datas_guard', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('data.get_datas_guard', page=page + 1)
        return jsonify({
            'datas': [data.to_full_json() for data in datas],
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
@api {GET} /data/guard 获取备用机数据
@apiGroup datas
@apiName 获取备用机数据

@apiParam (params) {String} sn 血糖仪sn码 
@apiParam (params) {String} date 数据日期_日期格式(0000-00-00)
@apiParam (params) {String} time 数据时间_时间格式(00:00:00)
@apiParam (params) {Number} glucose 血糖值
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
            "url":"数据地址",
            "glucose":"血糖值"
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


@data.route('/datas/<int:id>')
@login_required
def get_data(id):
    data = Data.query.get_or_404(id)
    return jsonify({
        'datas': [data.to_json()],
        'status': 'success',
        'reason': 'the data has been added'
    })


"""
@api {GET} /data/datas/<int:id> 根据id获取数据信息
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

@data.route('/guard/<int:id>', methods=['PUT'])
@login_required
def change_guard_data(id):
    data = GuargData.query.get_or_404(id)
    for k in request.json:
        if hasattr(data, k):
            setattr(data, k, request.json[k])
    try:
        db.session.add(data)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'reason': e,
            'data': []
        })
    return jsonify(data.to_full_json())

"""
@api {PUT} /data/gurad/<int:id> 根据id修改备用机数据
@apiGroup datas
@apiName 根据id修改备用机数据

@apiParam (params) {String} id 备用机数据id 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回修改后的备用机数据

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
            "url":"数据地址",
            "glucose":"血糖值"
        }],
        "status":"success",
        "reason":"there is the data"
    }
"""


@data.route('/guard/<int:id>', methods=['DELETE'])
@login_required
def delete_guard_data(id):
    data = GuargData.query.get_or_404(id)
    try:
        db.session.delete(data)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'reason': e,
            'data': []
        })
    return jsonify({
        'status':'success',
        'reason':''
    })

"""
@api {DELTET} /data/gurad/<int:id> 根据id删除备用机数据
@apiGroup datas
@apiName 根据id删除备用机数据

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

@data.route('/datas/guard/<int:id>')
@login_required
def get_guard_data(id):
    data = GuargData.query.filter(GuargData.data_id == id).first()
    return jsonify({
        'status':'success',
        'reason':'',
        'data': [data.to_full_json()]
    })

"""
@api {PUT} /data/gurad/<int:id> 根据id查询备用机数据
@apiGroup datas
@apiName 根据id查询备用机数据

@apiParam (params) {String} id 备用机数据id 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} datas 返回查询到的备用机数据

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
            "url":"数据地址",
            "glucose":"血糖值"
        }],
        "status":"success",
        "reason":"there is the data"
    }
"""


@data.route('/datas/<int:id>', methods=['PUT'])
@login_required
def change_data(id):
    data = Data.query.get_or_404(id)
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
            'url': url_for('data.get_data', id=data.data_id),
            'patient': url_for('data.get_patient', id=patient.patient_id),
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
@api {PUT} /data/datas/<int:id> 更改id所代表的数据的信息
@apiGroup datas
@apiName 更改id所代表的数据的信息

@apiParam (request) {String} id_number 医疗卡号(修改病人信息时添加)
@apiParam (request) {String} patient_name 病人姓名(修改病人信息时添加)
@apiParam (request) {String} sex 病人性别(修改病人信息时添加)
@apiParam (request) {String} tel 病人电话(修改病人信息时添加)
@apiParam (request) {Number} age 病人年龄(修改病人信息时添加)
@apiParam (request) {Number} doctor_id 医生id(修改病人信息时添加)
@apiParam (request) {String} sn 血糖仪sn码 
@apiParam (request) {String} date 数据日期_日期格式(0000-00-00)
@apiParam (request) {String} time 数据时间_时间格式(00:00:00)
@apiParam (request) {Number} glucose 血糖值
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
            "url":"数据地址",
            "glucose":"血糖值"
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


@data.route('/datas/<int:id>', methods=['DELETE'])
@login_required
def delete_data(id):
    data = Data.query.get_or_404(id)
    try:
        db.session.delete(data)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'reason': e
        })
    return jsonify({
        'status': 'success',
        'reason': 'the data has been deleted'
    }), 200


"""

@api {DELETE} /data/datas/<int:id> 删除id所代表的数据的信息
@apiGroup datas
@apiName 删除id所代表的数据的信息

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