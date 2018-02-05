from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for, current_app
from ..models import Patient, Operator, Data, Bed, Accuchek
from .authentication import auth

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
    for k in request.json:
        if hasattr(accuchek, k):
            setattr(accuchek, k, request.json[k])
