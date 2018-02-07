from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for, current_app
from ..models import Patient, Operator, Data, Bed, Accuchek, BedHistory
from .authentication import auth
from sqlalchemy.exc import OperationalError
import datetime

@api.route('/bedhistorys')
@auth.login_required
def get_histories():
    page = request.args.get('page', 1, type=int)
    fields = [i for i in BedHistory.__table__.c._data]
    bedhistorys = BedHistory.query
    for k, v in request.args.items():
        if k in fields:
            bedhistorys = bedhistorys.filter_by(**{k: v})
    if bedhistorys:
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
            'count': pagination.total
        })
    else:
        return jsonify({
            'status': 'fail',
            'reason': 'there is no data'
        })

@api.route('/bedhistorys', methods = ['POST'])
@auth.login_required
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
    return jsonify(bedhistory.to_json())

@api.route('/bedhistorys/<int:id>')
@auth.login_required
def get_history(id):
    bedhistory = BedHistory.query.get_or_404(id)
    return jsonify(bedhistory.to_json())

@api.route('/bedhistorys/<int:id>', methods = ['PUT'])
@auth.login_required
def change_history(id):
    bedhistory = BedHistory.query.get_or_404(id)
    if bedhistory.patient.doctor_id != g.current_user.operator_id:
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
    return jsonify(bedhistory.to_json())

@api.route('/bedhistorys/<int:id>', methods = ['DELETE'])
@auth.login_required
def delete_history(id):
    bedhistory = BedHistory.query.get_or_404(id)
    if bedhistory.patient.doctor_id != g.current_user.operator_id:
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
    return jsonify(bedhistory.to_json())