from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for, current_app
from ..models import Operator
from .authentication import auth
from sqlalchemy.exc import OperationalError

@api.route('/operators', methods = ['POST'])
def new_operator():
    tel = request.json['tel']
    operator = Operator.query.filter(Operator.tel == tel).first()
    if operator:
        return jsonify({
            'status':'fail',
            'reason':'the tel or the mail has been used'
        })
    operator = Operator.from_json(request.json)
    try:
        db.session.add(operator)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':operator.to_json()
        })
    return jsonify(operator.to_json())

@api.route('/operators')
@auth.login_required
def get_operators():
    operators = Operator.query
    fields = [i for i in Operator.__table__.c._data]
    for k, v in request.args.items():
        if k in fields:
            operators = operators.filter_by(**{k: v})
    if operators:
        page = request.args.get('page', 1, type=int)
        pagination = operators.paginate(page, per_page=current_app.config['PATIENTS_PRE_PAGE'], error_out=False)
        operators = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.get_patients', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('api.get_patients', page=page + 1)
        return jsonify({
            'operators': [operator.to_json() for operator in operators],
            'prev': prev,
            'next': next,
            'count': pagination.total
        })
    else:
        return jsonify({
            'status': 'fail',
            'reason': 'there is no data'
        })


@api.route('/operators/<int:id>')
@auth.login_required
def get_operator(id):
    operator = Operator.query.get_or_404(id)
    return jsonify(operator.to_json())


@api.route('/operators/<int:id>', methods = ['DELETE'])
@auth.login_required
def delete_operator(id):
    operator = Operator.query.get_or_404(id)
    if g.current_user.tel != operator.tel:
        return jsonify({
            'status':'fail',
            'reason':'no root'
        }), 403
    try:
        db.session.delete(operator)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':operator.to_json()
        })
    return jsonify(operator.to_json()), 200

@api.route('/operators/<int:id>', methods = ['PUT'])
@auth.login_required
def change_operator(id):
    operator = Operator.query.get_or_404(id)
    if g.current_user.tel != operator.tel:
        return jsonify({
            'status': 'fail',
            'reason': 'no root'
        }), 403
    for k in request.json:
        if hasattr(operator, k):
            setattr(operator, k, request.json[k])
    if 'password' in request.json:
        password = request.json['password']
        operator.password = password
    try:
        db.session.add(operator)
        db.session.commit()
    except OperationalError as e:
        return jsonify({
            'status':'fail',
            'reason':e,
            'data':operator.to_json()
        })
    return jsonify(operator.to_json()), 200

@api.route('/operators/now')
@auth.login_required
def get_operator_now():
    operator = g.current_user
    return jsonify(operator.to_json())

@api.route('/operators/now/password')
@auth.login_required
def operator_password():
    password = request.args.get('password')
    if g.current_user.verify_password(password):
        return jsonify(g.current_user.to_json()), 200
    else:
        return jsonify({
            'status':'fail',
            'reason':'wrong password'
        })

