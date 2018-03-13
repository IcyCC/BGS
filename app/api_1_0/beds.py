from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for, current_app
from ..models import Operator, Bed, Patient, Data, BedHistory
from .authentication import auth
from sqlalchemy.exc import OperationalError
import datetime
from ..decorators import allow_cross_domain
from flask_login import login_required, current_user


@api.route('/beds')


def get_beds():
    fields = [i for i in Bed.__table__.c._data]
    beds = Bed.query
    for k, v in request.args.items():
        if k in fields:
            beds = beds.filter_by(**{k: v})
    if beds:
        page = request.args.get('page', 1, type=int)
        pagination = beds.paginate(page, per_page=current_app.config['PATIENTS_PRE_PAGE'], error_out=False)
        beds = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.get_patients', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('api.get_patients', page=page + 1)
        return jsonify({
            'beds': [bed.to_json() for bed in beds],
            'prev': prev,
            'next': next,
            'count': pagination.total,
            'status': 'success',
            'reason': 'there are the datas'
        })
    else:
        return jsonify({
            'status': 'fail',
            'reason': 'there is no data'
        })


"""

@api {GET} /api/v1.0/beds 获取筛选beds信息
@apiGroup beds
@apiName 获取筛选beds信息

@apiParam (params) {String} id_number 医疗卡号
@apiParam (params) {String} sn 血糖仪sn码  
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} beds 返回经过筛选的beds信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "beds":[{
            "id_number":"患者医疗卡号",
            "sn":"血糖仪sn码",
            "url":"bed数据地址"
        }],
        "count":"总数量",
        "prev":"上一页地址",
        "next":"下一页地址",
        "reason":"there are the datas",
        "status":"success"
    }
    没有数据
    {
        "status":"fail",
        "reason":"there is no data"
    }

"""


@api.route('/beds', methods=['POST'])


def new_bed():
    bed = Bed()
    bedhistory = BedHistory()
    if 'sn' in request.json:
        sn = request.json['sn']
        bed = Bed.query.filter(Bed.sn == sn).first()
        if bed:
            return jsonify({
                'status': 'fail',
                'reason': 'the accu_chek has been used on the other bed'
            })
    if 'id_number' in request.json:
        id_number = request.json['id_number']
        bed = Bed.query.filter(Bed.id_number == id_number).first()
        if bed:
            return jsonify({
                'status': 'fail',
                'reason': 'the patient has been placed on the other bed'
            })
        else:
            bedhistory.id_number = id_number
            for k in request.json:
                if hasattr(bedhistory, k):
                    setattr(bedhistory, k, request.json[k])
    bed = Bed()
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
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'reason': e,
            'data': bed.to_json()
        })
    return jsonify({
        'beds': [bed.to_json()],
        'status': 'success',
        'reason': 'the data has been added'
    })


"""

@api {POST} /api/v1.0/beds 添加新的床位信息(json数据)
@apiGroup beds
@apiName 添加新的床位信息

@apiParam (params) {String} id_number 医疗卡号
@apiParam (params) {String} sn 血糖仪sn码  
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} beds 返回新添加的beds信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "beds":[{
            "id_number":"患者医疗卡号",
            "sn":"血糖仪sn码",
            "url":"床位数据地址"  
        }],
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


@api.route('/beds/<int:id>')


def get_bed(id):
    bed = Bed.query.get_or_404(id)
    return jsonify({
        'bed_information': [bed.bed_information()],
        'status': 'success',
        'reason': 'there is the data'
    })


"""

@api {GET} /api/v1.0/beds/<int:id> 获取id代表的beds信息
@apiGroup beds
@apiName 获取id代表的beds信息

@apiParam (params) {Number} id bed的id  
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} beds 返回id代表的bed的数据

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "bed_informaition":[{
            "id_number":"患者医疗卡号",
            "sn":"血糖仪sn码",
            "url":"bed数据地址",
            "tel":"患者电话",
            "sex":"患者性别",
            "patient_name":"患者姓名",
            "doctor_id":"医生id",
            "age":"患者年龄",
            "current_datas":[{
                "date":"数据日期",
                "glucose":"血糖",
                "id_number":"医疗卡号",
                "patient":"患者地址",
                "sn":"血糖仪sn码",
                "time":"数据时间",
                "url":"数据地址"
            }](最新的10个数据)
        }],
        "status":"success",
        "reason":"there is the data"


    }

"""


@api.route('/beds/<int:id>', methods=['DELETE'])


def delete_bed(id):
    bed = Bed.query.get_or_404(id)
    try:
        db.session.delete(bed)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'season': e,
            'data': bed.to_json()
        })
    return jsonify({
        'beds': [bed.to_json()],
        'status': 'success',
        'reason': 'the data has been deleted'
    }), 200


"""

@api {DELETE} /api/v1.0/beds/<int:id> 删除id所代表的床位信息
@apiGroup beds
@apiName 删除id所代表的床位信息

@apiParam (params) {Number} id 床位id
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} beds 返回删除的beds信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "beds":[{
            "id_number":"患者医疗卡号",
            "sn":"血糖仪sn码",
            "url":"床位数据地址"  
        }],
        "status":"success",
        "reason":"the data has been deleted"
    }

"""


@api.route('/beds/<int:id>', methods=['PUT'])


def change_bed(id):
    bed = Bed.query.get_or_404(id)
    bed_history = bed.bed_historys.order_by(Bed.bed_id.desc()).first()
    if 'sn' in request.json and request.json['sn']:
        sn = request.json['sn']
        may_bed = Bed.query.filter(Bed.sn == sn).first()
        if may_bed:
            if may_bed.bed_id != bed.bed_id:
                return jsonify({
                    'status': 'fail',
                    'reason': 'the accu_chek has been used on the other bed'
                })
    if 'id_number' in request.json and request.json['id_number']:
        id_number = request.json['id_number']
        may_bed = Bed.query.filter(Bed.id_number == id_number).first()
        if may_bed and may_bed.bed_id != bed.bed_id:
            return jsonify({
                'status': 'fail',
                'reason': 'the patient has been placed on the other bed'
            })
        if bed_history:
            if bed_history.id_number == request.json['id_number'] and bed_history.bed_id == id:
                for k in request.json:
                    if hasattr(bed_history, k):
                        setattr(bed_history, k, request.json[k])
        else:
            bed_history = BedHistory()
            for k in request.json:
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
        except OperationalError as e:
            return jsonify({
                'status': 'fail',
                'reason': e,
                'data': bed.to_json()
            })
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
                'data': patient.to_json()
            })
    if 'sn' in request.json and request.json['sn']:
        bed.sn = request.json['sn']
    for k in request.json:
        if hasattr(bed, k):
            setattr(bed, k, request.json[k])
    try:
        db.session.add(bed)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'reason': e,
            'data': bed.to_json()
        })
    return jsonify({
        'beds': [bed.to_json()],
        'status': 'success',
        'reason': 'the data has been changed'
    })


"""

@api {PUT} /api/v1.0/beds/<int:id> 修改id所代表的床位的信息
@apiGroup beds
@apiName 修改id所代表的床位的信息

@apiParam (params) {Number} id 床位号
@apiParam (params) {String} sn 血糖仪sn码
@apiParam (params) {String} id_number 医疗卡号
@apiParam (params) {String} patient_name 病人姓名
@apiParam (params) {String} sex 病人性别
@apiParam (params) {String} tel 病人电话
@apiParam (params) {Number} age 病人年龄
@apiParam (params) {Number} doctor_id 医生id  
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} beds 返回更改后的beds信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "beds":[{
            "id_number":"患者医疗卡号",
            "sn":"血糖仪sn码",
            "url":"床位数据地址"  
        }],
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


@api.route('/beds/<int:id>/more')


def get_bed_more(id):
    bed = Bed.query.get_or_404(id)
    patient = bed.patient
    return jsonify({
        'patient': patient.to_json(),
        'datas': url_for('api.get_bed_moredata', id=id),
        'beds': bed.to_json(),
        'status': 'success',
        'reason': 'there is the data'
    })


"""

@api {GET} /api/v1.0/beds/<int:id>/more 获取id所代表床位的全部信息
@apiGroup beds
@apiName 获取id所代表床位的全部信息

@apiParam (params) {Number} id 床位id 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} beds 返回id所代表床位的全部信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "bed":{
            "id_number":"患者医疗卡号",
            "sn":"血糖仪sn码",
            "url":"床位信息地址"
        },
        "datas":"床位所有数据的信息的地址",
        "patient":{
            "age":"患者年龄",
            "datas":"患者数据信息地址",
            "doctor_id":"医生id",
            "id_number":"医疗卡号",
            "patient_name":"患者姓名",
            "sex":"患者性别",
            "tel":"患者手机号",
            "url":"患者信息地址"
        },
        "reason":"there is the data",
        "status":"success"
    }

"""


@api.route('/beds/<int:id>/more_data')


def get_bed_moredatas(id):
    bed = Bed.query.get_or_404(id)
    datas = bed.datas.order_by(Data.date.desc(), Data.time.desc())
    if datas:
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
            'reason': 'there is the data'
        })
    else:
        return jsonify({
            'status': 'fail',
            'reason': 'there is no data'
        })


"""

@api {GET} /api/v1.0/beds/<int:id>/more_data 获取id所代表床位的全部数据的信息
@apiGroup beds
@apiName 获取id所代表床位的全部数据的信息

@apiParam (params) {Number} id 床位id 
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} beds 返回id所代表床位的全部数据的信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "datas":[{
            "date":"数据创建日期",
            "time":"数据创建时间",
            "glucose":"血糖值",
            "sn":"血糖仪sn码",
            "patient":"患者信息地址",
            "id_number":"医疗卡号",
            "url":"数据信息地址"
        }],
        "count":"总数量",
        "prev":"上一页地址",
        "next":"下一页地址",
        "pages":"总页数",
        "status":"success",
        "reason":"there is the data"
    }

"""


