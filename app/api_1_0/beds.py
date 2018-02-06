from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for, current_app
from ..models import Operator, Bed, Patient, Data, BedHistory
from .authentication import auth
from sqlalchemy.exc import OperationalError
import datetime

@api.route('/beds')
@auth.login_required
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
            'count': pagination.total
        })
    else:
        return jsonify({
            'status':'fail',
            'reason':'there is no data'
        })

@api.route('/beds', methods = ['POST'])
@auth.login_required
def new_bed():
    bed = Bed()
    bedhistory = BedHistory()
    if 'sn' in request.json:
        sn = request.json['sn']
        bed = Bed.query.filter(Bed.sn == sn).first()
        if bed:
            return jsonify({
                'status':'fail',
                'reason':'the accu_chek has been used on the other bed'
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
        db.session.commit()
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
    bed_history = bed.bed_historys.order_by(Bed.bed_id.desc()).first()
    if 'sn' in request.json and request.json['sn']:
        sn = request.json['sn']
        may_bed = Bed.query.filter(Bed.sn == sn).first()
        if may_bed:
            if may_bed.bed_id != bed.bed_id:
                return jsonify({
                    'status':'fail',
                    'reason':'the accu_chek has been used on the other bed'
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
                'status':'fail',
                'reason':e,
                'data':bed.to_json()
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
                'status':'fail',
                'reason':e,
                'data':patient.to_json()
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
    return jsonify(bed.to_json())

@api.route('/beds/<int:id>/more')
@auth.login_required
def get_bed_more(id):
    bed = Bed.query.get_or_404(id)
    patient = bed.patient
    return jsonify({
        'patient':patient.to_json(),
        'datas':url_for('api.get_bed_moredatas', id=id),
        'bed':bed.to_json()
    })

@api.route('/beds/<int:id>/more_datas')
@auth.login_required
def get_bed_moredatas(id):
    bed = Bed.query.get_or_404(id)
    datas = bed.datas
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

