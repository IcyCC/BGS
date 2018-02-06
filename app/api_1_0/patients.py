from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for, current_app
from ..models import Patient, Operator, Data, Bed
from .authentication import auth
from sqlalchemy.exc import OperationalError


@api.route('/patients', methods = ['POST'])
@auth.login_required
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
    return jsonify(patient.to_json())

@api.route('/patients')
@auth.login_required
def get_patients():
    page = request.args.get('page', 1, type=int)
    fields = [i for i in Patient.__table__.c._data]
    patients = Patient.query
    for k, v in request.args.items():
        if k in fields:
            patients = patients.filter_by(**{k: v})
    if patients:
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
            'count':pagination.total
        })
    else:
        return jsonify({
            'status':'fail',
            'reason':'there is no data'
        })

@api.route('/patients/<int:id>', methods = ['PUT'])
@auth.login_required
def change_patient(id):
    patient = Patient.query.get_or_404(id)
    doctor_id = patient.doctor_id
    if 'doctor_id' in request.json:
        doctor_id = request.json['doctor_id']
    if 'id_number' in request.json:
        id_number = request.json['id_number']
        may_patient = Patient.query.filter(Patient.id_number == id_number).first()
        if may_patient:
            if may_patient.patient_id != patient.patient_id:
                return jsonify({
                    'status':'fail',
                    'reason':'the id_number has been used'
                })
    if doctor_id != patient.doctor_id and g.current_user.operator_id != patient.doctor_id:
        return jsonify({
            'status':'fail',
            'reason':'no root'
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
    return jsonify(patient.to_json())

@api.route('/patients/<int:id>')
@auth.login_required
def get_patient(id):
    patient = Patient.query.get_or_404(id)
    return jsonify(patient.to_json())

@api.route('/patients/<int:id>', methods = ['DELETE'])
@auth.login_required
def delete_patients(id):
    patient = Patient.query.get_or_404(id)
    if g.current_user.operator_id != patient.doctor_id:
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
    return jsonify(patient.to_json())

@api.route('/patients/get-from-id')
@auth.login_required
def get_from_id():
    id_number = request.args.get('id_number')
    patient = Patient.query.filter(Patient.id_number == id_number).first()
    if patient:
        return jsonify(patient.to_json())
    else:
        return jsonify({
            'status':'fail'
        })

@api.route('/patients/<int:id>/datas')
@auth.login_required
def get_patient_datas(id):
    patient = Patient.query.get_or_404(id)
    datas = patient.datas
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
            'operators': [data.to_json() for data in datas],
            'prev': prev,
            'next': next,
            'count': pagination.total
        })
    else:
        return jsonify({
            'status': 'fail',
            'reason': 'there is no data'
        })


@api.route('/patients/history')
@auth.login_required
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
    end_date = request.args.get('end_time')
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
    if datas:
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
            'count': pagination.total
        })
    else:
        return jsonify({
            'status':'fail',
            'reason':'there is no reason'
        })


