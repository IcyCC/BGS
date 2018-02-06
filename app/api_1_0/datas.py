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
    data = Data()
    for k in request.json:
        if hasattr(data, k):
            setattr(data, k, request.json[k])
    if 'id_number' in request.json:
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
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time()
    data.date = date
    data.time = time
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
    if g.current_user.operator_id != data.patient.doctor_id:
        return jsonify({
            'status':'fail',
            'reason':'no root'
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
            'status':'fail',
            'reason':e,
            'data':data.to_json()
        })
    return jsonify({
        'url': url_for('api.get_data', id=data.data_id),
        'patient': url_for('api.get_patient', id=patient.patient_id),
        'sn': data.sn,
        'id_number': data.id_number,
        'time': str(data.time),
        'date': str(data.date),
        'glucose': data.glucose
    }), 200

@api.route('/datas/<int:id>', methods = ['DELETE'])
@auth.login_required
def delete_data(id):
    data = Data.query.get_or_404(id)
    if g.current_user.operator_id != data.patient.doctor_id:
        return jsonify({
            'status':'fail',
            'reason':'no root'
        })
    patient = data.patient
    try:
        db.session.delete(data)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':data.to_json()
        })
    return jsonify({
            'url':url_for('api.get_data', id = data.data_id),
            'patient':url_for('api.get_patient', id = patient.patient_id),
            'sn':data.sn,
            'id_number':data.id_number,
            'time':str(data.time),
            'date':str(data.date),
            'glucose':data.glucose
        }), 200