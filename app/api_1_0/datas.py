from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for, current_app
from ..models import Patient, Operator, Data, Bed, Accuchek
from .authentication import auth
import datetime
from sqlalchemy.exc import OperationalError

@api.route('/datas', methods = ['POST'])
@auth.login_required
def new_data():
    glucose = request.json['glucose']
    sn = request.json['sn']
    patient_name = request.json['patient_name']
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time()
    data = Data(date=date, time=time, glucose=glucose, sn=sn, patient_name=patient_name)
    try:
        db.session.add(data)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':data.to_json()
        })
    return jsonify(data.to_json())

@api.route('/datas')
@auth.login_required
def get_datas():
    data_fields = [i for i in Data.__table__.c._data]
    fields = data_fields
    datas = Data.query
    for k, v in request.args.items():
        if k in fields:
            datas = datas.filter_by(**{k: v})
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
            'count': pagination.total
        })
    else:
        return jsonify({
            'status':'fail',
            'reason':'there is no data'
        })

@api.route('/datas/<int:id>')
@auth.login_required
def get_data(id):
    data = Data.query.get_or_404(id)
    return jsonify(data.to_json())

@api.route('/datas/<int:id>', methods = ['PUT'])
@auth.login_required
def change_data(id):
    data = Data.query.get_or_404(id)
    if g.current_user.operator_name != data.patient.doctor_name:
        return jsonify({
            'status':'fail',
            'reason':'no root'
        })
    for k in request.json:
        if hasattr(data, k):
            setattr(data, k, request.json[k])
    try:
        db.session.add(data)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':data.to_json()
        })
    return jsonify(data.to_json())

@api.route('/datas/<int:id>', methods = ['DELETE'])
@auth.login_required
def delete_data(id):
    data = Data.query.get_or_404(id)
    if g.current_user.operator_name != data.patient.doctor_name:
        return jsonify({
            'status':'fail',
            'reason':'no root'
        })
    try:
        db.session.delete(data)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':data.to_json()
        })
    return jsonify(data.to_json()), 200