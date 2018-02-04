from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for
from ..models import Operator
from .authentication import auth

@api.route('/operators', methods = ['POST'])
def new_operator():
    operator = Operator.from_json(request.json)
    db.session.add(operator)
    db.session.commit()
    return 200

@api.route('/operators/<int:id>')
def get_operator(id):
    operator = Operator.query.get_or_404(id)
    return jsonify({
        operator.to_json()
    })


@api.route('/operators')
def get_operators():
    operators = Operator.query


@auth.login_required
@api.route('/operators/now')
def get_operator():
    operator = g.current_operator
    return jsonify(operator.to_json())

