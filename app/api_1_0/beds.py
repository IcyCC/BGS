from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for, current_app
from ..models import Operator, Bed, Patient, Data
from .authentication import auth
from sqlalchemy.exc import OperationalError


@api.route('/beds')
@auth.login_required
def get_beds():
    bed_fields = [i for i in Bed.__table__.c._data]
    patient_fileds = [i for i in Patient.__table__.c.data]
    fields = bed_fields + patient_fileds
    beds = Bed.query.join(Patient, Patient.patient_name == Bed.patient_name)
    for k, v in request.args.items():
        if k in fields:
            beds = beds.filter_by(**{k: v})
    if beds:
        page = request.args.get('page', 1, type=int)
        pagination = beds.paginate(page, per_page=current_app.config['PATIENTS_PRE_PAGE'], error_out=False)
        datas = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.get_patients', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('api.get_patients', page=page + 1)
        return jsonify({
            'datas': [data.to_json_data() for data in datas],
            'prev': prev,
            'next': next,
            'count': pagination.total
        })
    else:
        return 404

@api.route('/beds', methods = ['POST'])
@auth.login_required
def new_bed():
    bed = Bed()
    for k in request.json:
        if hasattr(bed, k):
            setattr(bed, k, request.json[k])
    try:
        db.session.add(bed)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':bed.to_json()
        })
    return jsonify(bed.to_json())

@api.route('/beds/<int:id>')
@auth.login_required
def get_bed(id):
    bed = Bed.query.get_or_404(id)
    return jsonify({
        'bed':bed.bed_information()
    })

@api.route('/beds/<int:id>', methods = ['DELETE'])
@auth.login_required
def delete_bed(id):
    bed = Bed.query.get_or_404(id)
    try:
        db.session.delete(bed)
        db.session.commite()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'season':e,
            'data':bed.to_json()
        })
    return jsonify(bed.to_json()), 200

@api.route('/beds/<int:id>', methods = ['PUT'])
@auth.login_required
def change_bed(id):
    bed = Bed.query.get_or_404(id)
    if request.json['patient_name']:
        bed.patient_name = request.json['patient_name']
        try:
            db.session.add(bed)
            db.session.commit()
        except OperationalError as e:
            return jsonify({
                'status':'fail',
                'reason':e,
                'data':bed.to_json()
            })
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

@api.route('/beds/<int:id>/more')
@auth.login_required
def get_bed_more(id):
    bed = Bed.query.get_or_404(id)
    all_data = bed.all_datas()
    patient = bed.patient
    return jsonify({
        'patient':patient.to_json(),
        'datas':[data.to_json() for data in all_data],
        'bed':bed.to_json()
    })

@api.route('/beds/<int:id>/more', methods = ['PUT'])
@auth.login_required
def change_bed_more(id):
    bed = Bed.query.get_or_404(id)
    all_data = bed.all_datas()
    change_datas = request.json['change_datas']
    for change_data in change_datas:
        id = change_data['id']
        time = change_data['time']
        date = change_data['date']
        glucose = change_data['glucose']
        data = all_data.filter(Data.id == id).first()
        if time:
            data.time = time
        if date:
            data.date = date
        if glucose:
            data.glucose = glucose
        db.session.add(data)
        db.session.commit()
    return 200

