from app.bed import bed_blueprint
from app import db
from flask import request, jsonify, url_for, current_app
from app.models import BedHistory
from sqlalchemy.exc import OperationalError
import datetime
from flask_login import login_required
import json

def std_json(d):
    r = {}
    for k, v in d.items():
        r[k] = json.loads(v)
    return r

@bed_blueprint.route('/bedhistorys')
@login_required
def get_histories():
    fields = [i for i in BedHistory.__table__.c._data]
    bedhistorys = BedHistory.query.order_by(BedHistory.date.desc(), BedHistory.time.desc())
    per_page = current_app.config['PATIENTS_PRE_PAGE']
    limit = None
    for k, v in std_json(request.args).items():
        if k in fields:
            bedhistorys = bedhistorys.filter_by(**{k: v})
        if k == 'per_page':
            per_page = v
        if k == 'limit':
            limit = v
    bedhistorys = bedhistorys.limit(limit).from_self() if limit is not None else bedhistorys.from_self()
    page = request.args.get('page', 1, type=int)
    pagination = bedhistorys.paginate(page, per_page=per_page, error_out=False)
    bedhistorys = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('bed_blueprint.get_histories', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('bed_blueprint.get_histories', page=page + 1)
    return jsonify({
        'bedhistorys': [bedhistory.to_json() for bedhistory in bedhistorys],
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

@api {GET} /bedhistorys 获取筛选所有的床位历史信息
@apiGroup beds
@apiName 获取筛选所有的床位历史信息

@apiParam (params) {Number} bed_id 床位id
@apiParam (params) {String} date 床位历史日期_日期格式(0000-00-00)
@apiParam (params) {String} time 床位历史时间_时间模式(00:00:00)
@apiParam (params) {String} id_number 医疗卡号
@apiParam (params) {String} sn 血糖仪sn码
@apiParam (params) {Number} limit 查询总数量
@apiParam (params) {Number} per_page 每一页的数量
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} bedhistorys 返回筛选过的床位历史信息信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "bedhistorys":[{
            "history_id":"历史信息id",
            "bed_id":"床位号",
            "time":"历史信息时间",
            "date":"历史信息日期",
            "sn":"血糖仪sn码",
            "id_number":"医疗卡号"
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


@bed_blueprint.route('/bedhistorys', methods = ['POST'])
@login_required

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

@api {POST} /bedhistorys 新建床位历史信息
@apiGroup beds
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
            "history_id":"历史信息id",
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


@bed_blueprint.route('/bedhistorys/<int:id>')
@login_required
def get_history(id):
    bedhistory = BedHistory.query.get_or_404(id)
    return jsonify({
        "bedhistorys": bedhistory.to_json(),
        "status": "success",
        "reason": "there is the data"
    })

"""

@api {GET} /bedhistorys/<int:id> 获取id所代表的床位历史的信息
@apiGroup beds
@apiName 获取id所代表的床位历史的信息

@apiParam (params) {Number} id 床位历史信息id
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} bedhistorys 返回id所代表的床位历史信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "bedhistorys":[{
            "history_id":"历史信息id",
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


@bed_blueprint.route('/bedhistorys/<int:id>', methods = ['PUT'])
@login_required

def change_history(id):
    bedhistory = BedHistory.query.get_or_404(id)
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

@api {PUT} /bedhistorys/<int:id> 更改id所代表的床位历史的信息
@apiGroup beds
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
            "history_id":"历史信息id",
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


@bed_blueprint.route('/bedhistorys/<int:id>', methods = ['DELETE'])
@login_required

def delete_history(id):
    bedhistory = BedHistory.query.get_or_404(id)
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

@api {DELETE} /bedhistorys/<int:id> 删除id所代表的床位历史的信息
@apiGroup beds
@apiName 删除id所代表的床位历史的信息

@apiParam (params) {Number} id 床位历史信息id
@apiParam (Login) {String} login 登录才可以访问

@apiSuccess {Array} bedhistorys 返回删除的的床位历史的信息

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "bedhistorys":[{
            "history_id":"历史信息id",
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
