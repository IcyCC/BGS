from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for, current_app
from ..models import Patient, Operator, Data, Bed, Accuchek
from .authentication import auth
from sqlalchemy.exc import OperationalError,IntegrityError

@api.route('/accucheks')
@auth.login_required
def get_accunckes():
    fields = [i for i in Accuchek.__table__.c._data]
    accunckes = Accuchek.query
    for k, v in request.args.items():
        if k in fields:
            accunckes = accunckes.filter_by(**{k: v})
    if accunckes:
        page = request.args.get('page', 1, type=int)
        pagination = accunckes.paginate(page, per_page=current_app.config['PATIENTS_PRE_PAGE'], error_out=False)
        accunckes = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.get_patients', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('api.get_patients', page=page + 1)
        return jsonify({
            'accunckes': [accuncke.to_json() for accuncke in accunckes],
            'prev': prev,
            'next': next,
            'count': pagination.total
        })
    else:
        return jsonify({
            'status':'fail',
            'reason':'there is no data'
        })

@api.route('/accucheks', methods = ['POST'])
@auth.login_required
def new_accuchek():
    accuchek = Accuchek()
    if 'sn' in request.json:
        sn = request.json['sn']
        may_accuchek = Accuchek.query.filter(Accuchek.sn == sn).first()
        if may_accuchek:
            return jsonify({
                'status':'fail',
                'reason':'the sn has been used'
            })
    for k in request.json:
        if hasattr(accuchek, k):
            try:
                setattr(accuchek, k, request.json[k])
            except IntegrityError as e:
                return jsonify({
                    'status':'fail',
                    'reason':e
                })
    try:
        db.session.add(accuchek)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':accuchek.to_json()
        })
    return jsonify(accuchek.to_json())

@api.route('/accucheks/<int:id>')
@auth.login_required
def get_accuchek(id):
    accuchek = Accuchek.query.get_or_404(id)
    return jsonify(accuchek.to_json())

@api.route('/accucheks/<int:id>', methods = ['DELETE'])
@auth.login_required
def delete_accuchek(id):
    accuchek = Accuchek.query.get_or_404(id)
    try:
        db.session.delete(accuchek)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e
        })
    return jsonify(accuchek.to_json())

@api.route('/accucheks/<int:id>', methods = ['PUT'])
@auth.login_required
def change_accuchek(id):
    accuchek = Accuchek.query.get_or_404(id)
    if 'sn' in request.json:
        sn = request.json['sn']
        may_accuchek = Accuchek.query.filter(Accuchek.sn == sn).first()
        if may_accuchek.accuchek_id != id:
            return jsonify({
                'status':'fail',
                'reason':'the sn has been used'
            })
    for k in request.json:
        if hasattr(accuchek, k):
            setattr(accuchek, k, request.json[k])
    try:
        db.session.add(accuchek)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e
        })
    return jsonify(accuchek.to_json())




