from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for
from ..models import Operator, Bed, Patient, Data
from .authentication import auth

@auth.login_required
@api.route('/beds')
def get_beds():
    beds = Bed.query
    return jsonify({
        'beds':[bed.bed_information() for bed in beds]
    })

@auth.login_required
@api.route('/beds/<int:id>')
def get_bed(id):
    bed = Bed.query.get_or_404(id)
    return jsonify({
        'bed':bed.bed_information()
    })

@auth.login_required
@api.route('/beds/<int:id>/more')
def get_bed_more(id):
    bed = Bed.query.get_or_404(id)
    all_data = bed.all_datas()
    patient = bed.patient
    return jsonify({
        'patient':patient.to_json(),
        'datas':[data.to_json() for data in all_data],
        'bed':bed.to_json()
    })

@auth.login_required
@api.route('/beds/<int:id>/more', methods = ['PUT'])
def change_bed_more(id):
    bed = Bed.query.get_or_404(id)
    all_data = bed.all_datas()
    change_datas = request.json['change_datas']
    for change_data in change_datas:
        id = change_data['id']
        time = change_data['time']
        date = change_data['date']
        glucose = change_data['glucose']
        data = all_data.filter_by(Data.id == id).first()
        if time:
            data.time = time
        if date:
            data.date = date
        if glucose:
            data.glucose = glucose
        db.session.add(data)
        db.session.commit()
    return 200

@auth.login_required
@api.route('/beds/<int:id>', methods = ['PUT'])
def change_bed(id):
    bed = Bed.query.get_or_404(id)
    if request.json['patient_name']:
        bed.patient_name = request.json['patient_name']
        db.session.add(bed)
        db.session.commit()
        bed.patient.patient_name = request.json['patient_name']
        bed.patient.sex = request.json['sex']
        bed.patient.tel = request.json['tel']
        bed.patient.age = request.json['age']
        bed.patient.doctor_name = request.json['doctor_name']
        db.session.add(bed.patient)
        db.session.commit()
    if request.json['sn']:
        bed.sn = request.json['sn']
    db.session.add(bed)
    db.session.commit()
    return 200