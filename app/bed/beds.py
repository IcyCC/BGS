from app.bed import bed_blueprint
from app import db
from flask import request, jsonify, url_for, current_app, abort
from app.models import Bed, Patient, Data, BedHistory
from sqlalchemy.exc import IntegrityError
import datetime
from flask_login import login_required
import json
from app.models import InvalidUsage
from marshmallow.exceptions import ValidationError
from app.form_model import GetBedValidation, BedValidation, BedMoreDataValidation, ChangeBedValidation

def std_json(d):
    r = {}
    for k, v in d.items():
        try:
            r[k] = json.loads(v)
        except:
            r[k] = v
    return r

@bed_blueprint.route('/beds')
@login_required
def get_beds():
    params_dict = {
        'sn': request.args.get('sn', None, type=str),
        'per_page': request.args.get('per_page', None, type=int),
        'limit': request.args.get('limit', None, type=int),
        'bed_id': request.args.get('bed_id', None, type=int),
        'page': request.args.get('page', None, type=int),
        'patient_id': request.args.get('patient_id',None, type=int)
    }
    try:
        GetBedValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    fields = [i for i in Bed.__table__.c._data]
    beds = Bed.query
    limit = None
    per_page = current_app.config['PATIENTS_PRE_PAGE']
    for k, v in std_json(request.args).items():
        if k in fields:
            beds = beds.filter_by(**{k: v})
        if k == 'per_page':
            per_page = v
        if k == 'limit':
            limit = v
    beds = beds.limit(limit).from_self() if limit is not None else beds.from_self()
    page = request.args.get('page', 1, type=int)
    pagination = beds.paginate(page, per_page=per_page, error_out=False)
    beds = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('bed_blueprint.get_beds', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('bed_blueprint.get_beds', page=page + 1)
    return jsonify({
        'beds': [bed.bed_full_data() for bed in beds],
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

@api {GET} /beds 获取筛选beds信息
@apiGroup beds

@apiParam (params) {Int} bed_id 病床号码
@apiParam (params) {Int} patient_id 病人id
@apiParam (params) {Int} limit 查询总数量
@apiParam (params) {Int} per_page 每页数量
@apiParam (params) {String} sn 血糖仪sn码  
@apiParam (params) {Int} page 当前页数
@apiParam (Login) {String} login 登录才可以访问

@apisuccess {Array} beds 返回经过筛选的beds信息(返回的是全部数据)

@apisuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "beds":[{
                "bed_id": "床位id",
                "patient_id": "病人id",
                "sn": "血糖仪sn码",
                "patient":{
                    "doctor_name": "医生姓名",
                    "id_number": "患者医疗卡号",
                    "patient_id": "患者id",
                    "patient_name": "患者姓名",
                    "sex": "患者性别",
                    "age":"患者年龄",
                    "tel":"患者电话"
                },
                "datas":[{
                    "data_id": "数据id",
                    "date": "数据日期",
                    "glucose": "血糖值",
                    "patient_id":"患者id",
                    "id_number": "患者医疗卡号",
                    "sn": "血糖仪sn码",
                    "time": "数据时间"
                }]
            }],
            "sn":"血糖仪sn码",
            "bed_id":"床位号"
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


@bed_blueprint.route('/beds', methods=['POST'])
@login_required
def new_bed():
    params_dict = {
        'sn': request.json.get('sn', None),
        'bed_id': request.json.get('bed_id', None),
        'patient_id': request.json.get('patient_id', None)
    }
    try:
        BedValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    bed = Bed()
    bedhistory = BedHistory()
    if 'sn' in request.json:
        sn = request.json['sn']
        maybed_sn = bed.query.filter(Bed.sn == sn).first()
        if maybed_sn:
            return jsonify({
                'status': 'fail',
                'reason': '血糖仪已经被使用在了其他床位'
            })
    if 'patient_id' in request.json:
        patient_id = request.json['patient_id']
        mayed_id = bed.query.filter(Bed.patient_id == patient_id).first()
        if mayed_id:
            return jsonify({
                'status': 'fail',
                'reason': '病人已经被安置在其他床位'
            })
        else:
            bedhistory.patient_id = patient_id
            for k in request.json:
                if hasattr(bedhistory, k):
                    setattr(bedhistory, k, request.json[k])
    for k in request.json:
        if hasattr(bed, k):
            setattr(bed, k, request.json[k])
    try:

        db.session.add(bed)
        db.session.commit()
        bedhistory.bed_id = bed.bed_id
        date = datetime.datetime.now().date()
        time = datetime.datetime.now().time()
        bedhistory.date = date
        bedhistory.time = time
        db.session.add(bedhistory)
        db.session.commit()
    except IntegrityError as e:
        raise InvalidUsage(message=str(e), status_code=500)
    return jsonify({
        'bed': bed.to_json(),
        'status': 'success',
        'reason': '数据已经被添加'
    })


"""

@api {POST} /beds 添加新的床位信息(json数据)
@apiGroup beds

@apiParam (json) {Int} patient_id 病人id
@apiParam (json) {String} sn 血糖仪sn码  
@apiParam (Login) {String} login 登录才可以访问

@apisuccess {Array} beds 返回新添加的beds信息(返回的是床位信息不带数据)

@apisuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "bed":{
            "patient_id":"患者id",
            "sn":"血糖仪sn码",
            "bed_id":"床位数据地址"  
        },
        "status":"success",
        "reason":"the data has been added"
    }
    病人已经被安排在其他床上
    {
        "status":"fail",
        "reason":"the patient has been placed on the other bed"
    }
    血糖仪被用在其他床位
    {
        "status":"fail",
        "reason":"the accu_chek has been used on the other bed"
    }

"""


@bed_blueprint.route('/beds/<int:id>')
@login_required
def get_bed(id):
    bed = Bed.query.get_or_404(id)
    return jsonify({
        'bed': bed.to_json(),
        'status': 'success',
        'reason': '这是查询到的数据'
    })


"""

@api {GET} /beds/<int:id> 返回id代表的bed的数据(带最近10组数据)
@apiGroup beds

@apiParam (params) {Int} id bed的id  
@apiParam (Login) {String} login 登录才可以访问

@apisuccess {Array} beds 返回id代表的bed的数据(带最近10组数据)

@apisuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "bed":{
            'bed_id':'床位id',
            'patient_id':'患者id',
            'sn':'血糖仪sn码'
        },
        "status":"success",
        "reason":"there is the data"
    }

"""


@bed_blueprint.route('/beds/<int:id>', methods=['DELETE'])
@login_required
def delete_bed(id):
    bed = Bed.query.get_or_404(id)
    bedhistorys = bed.bed_historys.all()
    try:
        db.session.delete(bed)
        db.session.commit()
    except IntegrityError as e:
        raise InvalidUsage(message=str(e), status_code=500)
    for bedhistory in bedhistorys:
        print(bedhistory.time)
        try:
            db.session.delete(bedhistory)
            db.session.commit()
        except IntegrityError as e:
            raise InvalidUsage(message=str(e), status_code=500)
    return jsonify({
        'status': 'success',
        'reason': '数据已经被删除了'
    }), 200


"""

@api {DELETE} /beds/<int:id> 删除id所代表的床位信息
@apiGroup beds

@apiParam (params) {Int} id 床位id
@apiParam (Login) {String} login 登录才可以访问

@apisuccess {Array} status 返回删除状态

@apisuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "status":"success",
        "reason":"the data has been deleted"
    }
    {
        "status":"fail",
        "reason":""
    }
"""


@bed_blueprint.route('/beds/<int:id>', methods=['PUT'])
@login_required
def change_bed(id):
    params_dict = {
        'patient_id': request.json.get('patient_id', None),
        'sn': request.json.get('sn', None),
        'bed_id': request.json.get('bed_id', None)
    }
    try:
        ChangeBedValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    bed = Bed.query.get_or_404(id)
    if 'sn' in request.json and request.json['sn']:
        sn = request.json['sn']
        may_bed = bed.query.filter(Bed.sn == sn).first()
        if may_bed:
            if may_bed.bed_id != bed.bed_id:
                return jsonify({
                    'status': 'fail',
                    'reason': '血糖仪已经被用在其他床位上了'
                })
    if 'patient_id' in request.json and request.json['patient_id']:
        patient_id = request.json['patient_id']
        may_bed = bed.query.filter(Bed.patient_id == patient_id).first()
        if may_bed and may_bed.bed_id != bed.bed_id:
            return jsonify({
                'status': 'fail',
                'reason': '病人已经被安置在了其他床位上'
            })
    bed_history = BedHistory()
    for k in    request.json:
        if hasattr(bed_history, k):
            setattr(bed_history, k, request.json[k])
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time()
    bed_history.bed_id = id
    bed_history.date = date
    bed_history.time = time
    try:
        db.session.add(bed_history)
        db.session.add(bed)
        db.session.commit()
    except IntegrityError as e:
        raise InvalidUsage(message=str(e), status_code=500)
    for k in request.json:
        if hasattr(bed, k):
            setattr(bed, k, request.json[k])
    try:
        db.session.add(bed)
        db.session.commit()
    except IntegrityError as e:
        raise InvalidUsage(message=str(e), status_code=500)
    return jsonify({
        'bed': bed.to_json(),
        'status': 'success',
        'reason': '数据已经被更改了'
    })


"""

@api {PUT} /beds/<int:id> 修改id所代表的床位的信息
@apiGroup beds

@apiParam (params) {Int} id 床位号
@apiParam (json) {String} sn 血糖仪sn码
@apiParam (json) {Int} patient_id 病人id
@apiParam (Login) {String} login 登录才可以访问

@apisuccess {Array} beds 返回更改后的beds信息

@apisuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "bed":{
            "patient_id":"患者id",
            "sn":"血糖仪sn码",
            "bed_id":"床位数据地址"  
        },
        "status":"success",
        "reason":"the data has been changed"
    }
    病人已经被安排在其他床
    {
        "status":"fail",
        "reason":"the patient has been placed on the other bed"
    }
    血糖仪已经被用在其他床位
    {
        "status":"fail",
        "reason":"the accu_chek has been used on the other bed"
    }
"""


@bed_blueprint.route('/beds/<int:id>/patient')
@login_required

def get_bed_more(id):
    bed = Bed.query.get_or_404(id)
    patient = bed.patient
    return jsonify({
        'patient': patient.to_json() if patient is not None else [],
        'status': 'success',
        'reason': '这里是查询到的数据'
    })


"""

@api {GET} /beds/<int:id>/patient 获取id所代表床位的病人信息(不包括数据信息)
@apiGroup beds

@apiParam (params) {Int} id 床位id 
@apiParam (Login) {String} login 登录才可以访问

@apisuccess {Array} beds 返回id所代表床位的全部信息

@apisuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "datas_url":"床位所有数据的信息的地址",
        "patient":{
            "age":"患者年龄",
            "datas_url":"患者数据信息地址",
            "doctor_id":"医生id",
            "id_number":"医疗卡号",
            "patient_name":"患者姓名",
            "sex":"患者性别",
            "tel":"患者手机号",
            "patient_id":"患者id"
        },
        "reason":"there is the data",
        "status":"success"
    }

"""


@bed_blueprint.route('/beds/<int:id>/datas')
@login_required
def get_bed_moredatas(id):
    params_dict = {
        'patient_id': request.args.get('patient_id', None, type=int),
        'data_id': request.args.get('data_id', None, type=int),
        'glucose': request.args.get('glucose', None, type=float),
        'hidden': request.args.get('hidden', None, type=bool),
        'sn': request.args.get('sn', None, type=str),
        'time': request.args.get('time', None, type = str),
        'date': request.args.get('date', None, type=str),
        'per_page': request.args.get('per_page', None, type=int),
        'limit': request.args.get('limit', None, type=int),
        'page': request.args.get('page', None, type=int)
    }
    try:
        BedMoreDataValidation().load(params_dict)
    except ValidationError as e:
        return jsonify({
            'status': 'fail',
            'reason': str(e)
        })
    bed = Bed.query.get_or_404(id)
    datas = bed.datas.order_by(Data.date.desc(), Data.time.desc())
    per_page = current_app.config['PATIENTS_PRE_PAGE']
    fields = [i for i in Data.__table__.c._data]
    limit = None
    for k, v in std_json(request.args).items():
        if k in fields:
            field = getattr(Data, k)
            datas = datas.filter(field == v)
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
        prev = url_for('bed_blueprint.get_bed_moredatas', id = id,page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('bed_blueprint.get_bed_moredatas', id = id, page=page + 1)
    return jsonify({
        'patient': bed.patient.to_json_patient(),
        'datas': [data.to_json_without_patient() for data in datas],
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

@api {GET} /beds/<int:id>/datas 获取id所代表床位的当前病人信息
@apiGroup beds

@apiParam (params) {Int} id 床位id 
@apiParam (params) {Int} limit 查询总数量
@apiParam (params) {Int} per_page 每一页的数量
@apiParam (params) {Bool} hidden 数据是否隐藏(0:未隐藏, 1:隐藏)
@apiParam (params) {Int} page 当前页数
@apiParam (params) {Int} patient_id 患者id
@apiParam (params) {String} id_number 患者医疗卡号 
@apiParam (params) {Int} data_id 数据id 
@apiParam (params) {Float} glucose 血糖值
@apiParam (params) {String} sn 血糖仪sn码
@apiParam (params) {Time} time 数据时间
@apiParam (params) {Date} date 数据日期 
@apiParam (Login) {String} login 登录才可以访问


@apisuccess {Array} beds 返回id所代表床位的全部数据的信息

@apisuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "datas":[{
            "data_id": "数据id",
            "date": "数据日期",
            "glucose": "血糖值",
            "id_number": "病人医疗卡号",
            "sn": "血糖仪sn码",
            "time": "血糖仪日期"
        }],
        "patient":{
            "doctor_name": "医生姓名",
            "id_number": "患者医疗卡号",
            "patient_id": "患者id",
            "patient_name": "患者姓名",
            "sex": "患者性别",
            "age":"患者年龄",
            "tel":"患者电话"
        }
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


