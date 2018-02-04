from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for
from ..models import Patient, Operator, Data, Bed
from .authentication import auth

@auth.login_required
@api.route('/patients', methods = ['POST'])
def new_patient():
    patient = Patient.from_json(request.json)
    db.session.add(patient)
    db.session.commit()
    return 200

@api.route('/patients')
def get_all_patients():
    patients = Patient.query
    return jsonify({
        'patients':[patient.to_json() for patient in patients]
    })

@auth.login_required
@api.route('/patients/get-from-id', methods = ['POST'])
def get_from_id():
    patient = Patient.query.filter_by(Patient.id_number == request.json['id_number'])
    return jsonify(patient.to_json_data())

@auth.login_required
@api.route('/patients/history')
def patients_history():
    patients = Patient.query.join(Data, Data.patient_name == Patient.patient_name)
    return jsonify({
        'patients': [patient.to_json_data() for patient in patients]
    })

@auth.login_required
@api.route('/patients/history', methods = ['POST'])
def patients_history_part():
    patients = Patient.query.join(Data, Data.patient_name == Patient.patient_name)
    patient_name = request.json['patient_name']
    sex = request.json['sex']
    age = request.json['age']
    tel = request.json['tel']
    id_number = request.json['id_number']
    max_age = request.json['max_age']
    min_age = request.json['min_age']
    max_glucose = request.json['max_glucose']
    min_glucose = request.json['min_glucose']
    begin_time = request.json['begin_time']
    end_time = request.json['end_time']
    if patient_name:
        patients = patients.filter_by(Patient.patient_name == patient_name)
    if sex:
        patients = patients.filter_by(Patient.sex == sex)
    if age:
        patients = patients.filter_by(Patient.age == age)
    if tel:
        patients = patients.filter_by(Patient.tel == tel)
    if id_number:
        patients = patients.filter_by(Patient.id_number == id_number)
    if max_age:
        patients = patients.filter_by(Patient.age <= max_age)
    if min_age:
        patients = patients.filter_by(Patient.age >= min_age)
    if max_glucose:
        patients = patients.filter_by(Data.glucose <= max_glucose)
    if min_glucose:
        patients = patients.filter_by(Data.glucose >= min_glucose)
    if begin_time:
        patients = patients.filter_by(Data.time >= begin_time)
    if end_time:
        patients = patients.filter_by(Data.time <= end_time)
    return jsonify({
        'patients':[patient.to_json_data() for patient in patients]
    })


