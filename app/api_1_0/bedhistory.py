from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for, current_app
from ..models import Patient, Operator, Data, Bed, Accuchek, BedHistory
from .authentication import auth
from sqlalchemy.exc import OperationalError
import datetime
from ..decorators import allow_cross_domain
from flask_login import login_required, current_user

@api.route('/bedhistorys')

@allow_cross_domain
def get_histories():
    page = request.args.get('page', 1, type=int)
    fields = [i for i in BedHistory.__table__.c._data]
    bedhistorys = BedHistory.query
    for k, v in request.args.items():
        if k in fields:
            bedhistorys = bedhistorys.filter_by(**{k: v})
    bedhistorys = bedhistorys.order_by(BedHistory.date.desc(), BedHistory.time.desc())
    if bedhistorys.count()!=0:
        pagination = bedhistorys.paginate(page, per_page=current_app.config['PATIENTS_PRE_PAGE'], error_out=False)
        bedhistorys = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.get_patients', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('api.get_patients', page=page + 1)
        return jsonify({
            'bedhistorys': [bedhistory.to_json() for bedhistory in bedhistorys],
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

@api {GET} /api/v1.0/bedhistorys 获取筛选所有的床位历史信息
@apiGroup bedhistorys
@apiName 获取筛选所有的床位历史信息

@apiParam (params) {Number} bed_id 床位id
@apiParam (params) {String} date 床位历史日期_日期格式(0000-00-00)
@apiParam (params) {String} time 床位历史时间_时间模式(00:00:00)
@apiParam (params) {String} id_number 医疗卡号
@apiParam (params) {String} sn 血糖仪sn码
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} bedhistorys 返回筛选过的床位历史信息信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        “bedhistorys”:[{
            "url":"历史信息地址",
            "bed_id":"床位号",
            "time":"历史信息时间",
            "date":"历史信息日期",
            "sn":"血糖仪sn码",
            "id_number":"医疗卡号"
        }],
        "prev":"上一页地址",
        "next":"下一页地址",
        "count":"总数量",
        "pages":"总页数",
        "status":"success":
        "reason":"there are the datas"
    }
    没有数据
    {
        "status":"fail",
        "reason":"there is no data"
    }
"""


@api.route('/bedhistorys', methods = ['POST'])

@allow_cross_domain
def new_history():
    bedhistory = BedHistory()
    for k in request.json:
        if hasattr(bedhistory, k):
            setattr(bedhistory, k, request.json[k])
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time()
    bedhistory.date = date
    bedhistory.time = time
    try:
        db.session.add(bedhistory)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e
        })
    return jsonify({
        "bedhistorys":bedhistory.to_json(),
        "status":"success",
        "reason":"the data has been added"
    })

"""

@api {POST} /api/v1.0/bedhistorys 新建床位历史信息
@apiGroup bedhistorys
@apiName 新建床位历史信息

@apiParam (params) {Number} bed_id 床位id
@apiParam (params) {String} date 床位历史日期_日期格式(0000-00-00)
@apiParam (params) {String} time 床位历史时间_时间模式(00:00:00)
@apiParam (params) {String} id_number 医疗卡号
@apiParam (params) {String} sn 血糖仪sn码
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} bedhistorys 返回新建的床位历史信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "bedhistorys":[{
            "url":"历史信息地址",
            "bed_id":"床位号",
            "time":"历史信息时间",
            "date":"历史信息日期",
            "sn":"血糖仪sn码",
            "id_number":"医疗卡号"  
        }],
        "status":"success",
        "reason":"the data has been added"
    }

"""


@api.route('/bedhistorys/<int:id>')

@allow_cross_domain
def get_history(id):
    bedhistory = BedHistory.query.get_or_404(id)
    return jsonify({
        "bedhistorys": bedhistory.to_json(),
        "status": "success",
        "reason": "there is the data"
    })

"""

@api {GET} /api/v1.0/bedhistorys/<int:id> 获取id所代表的床位历史的信息
@apiGroup bedhistorys
@apiName 获取id所代表的床位历史的信息

@apiParam (params) {Number} id 床位历史信息id
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} bedhistorys 返回id所代表的床位历史信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "bedhistorys":[{
            "url":"历史信息地址",
            "bed_id":"床位号",
            "time":"历史信息时间",
            "date":"历史信息日期",
            "sn":"血糖仪sn码",
            "id_number":"医疗卡号"  
        }],
        "status":"success",
        "reason":"there is the data"
    }

"""


@api.route('/bedhistorys/<int:id>', methods = ['PUT'])

@allow_cross_domain
def change_history(id):
    bedhistory = BedHistory.query.get_or_404(id)
    if bedhistory.patient.doctor_id != current_user.id:
        return jsonify({
            'status':'fail',
            'reason':'no root'
        })
    for k in request.json:
        if hasattr(bedhistory, k):
            setattr(bedhistory, k ,request.json[k])
    try:
        db.session.add(bedhistory)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e
        })
    return jsonify({
        "bedhistorys": bedhistory.to_json(),
        "status": "success",
        "reason": "the data has been changed"
    })

"""

@api {PUT} /api/v1.0/bedhistorys/<int:id> 更改id所代表的床位历史的信息
@apiGroup bedhistorys
@apiName 更改id所代表的床位历史的信息

@apiParam (params) {Number} bed_id 床位id
@apiParam (params) {String} date 床位历史日期_日期格式(0000-00-00)
@apiParam (params) {String} time 床位历史时间_时间模式(00:00:00)
@apiParam (params) {String} id_number 医疗卡号
@apiParam (params) {String} sn 血糖仪sn码
@apiParam (params) {Number} id 床位历史信息id
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} bedhistorys 返回更改的床位历史信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "bedhistorys":[{
            "url":"历史信息地址",
            "bed_id":"床位号",
            "time":"历史信息时间",
            "date":"历史信息日期",
            "sn":"血糖仪sn码",
            "id_number":"医疗卡号"  
        }],
        "status":"success",
        "reason":"the data has been changed"
    }
    不是主治医师修改
    {
        "status":"fail",
        "reason":"no root"
    }
"""


@api.route('/bedhistorys/<int:id>', methods = ['DELETE'])

@allow_cross_domain
def delete_history(id):
    bedhistory = BedHistory.query.get_or_404(id)
    if bedhistory.patient.doctor_id != current_user.id:
        return jsonify({
            'status': 'fail',
            'reason': 'no root'
        })
    try:
        db.session.delete(bedhistory)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status': 'fail',
            'reason': e
        })
    return jsonify({
        "bedhistorys": bedhistory.to_json(),
        "status": "success",
        "reason": "the data has been deleted"
    })


"""

@api {DELETE} /api/v1.0/bedhistorys/<int:id> 删除id所代表的床位历史的信息
@apiGroup bedhistorys
@apiName 删除id所代表的床位历史的信息

@apiParam (params) {Number} id 床位历史信息id
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} bedhistorys 返回删除的的床位历史的信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "bedhistorys":[{
            "url":"历史信息地址",
            "bed_id":"床位号",
            "time":"历史信息时间",
            "date":"历史信息日期",
            "sn":"血糖仪sn码",
            "id_number":"医疗卡号"  
        }],
        "status":"success",
        "reason":"the data has been deleted"
    }
    不是主治医师删除
    {
        "status":"fail",
        "reason":"no root"
    }

"""
