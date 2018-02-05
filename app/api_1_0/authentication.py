from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth
from ..models import Operator
from . import api

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(operatorname_or_token, password):
    if password == "":
        operator = Operator.verify_auth_token(operatorname_or_token)
        if operator is None:
            return False
        else:
            g.current_user = operator
            return True
    else:
        operator = Operator.query.filter(Operator.tel == operatorname_or_token).first()
        if operator.verify_password(password):
            g.current_user = operator
            return True
        else:
            return False

@api.route('/login')
def operator_login():
    tel = request.args.get('tel')
    password = request.json['password']
    operator = Operator.query.filter(Operator.tel == tel)
    if operator.verify_password(password):
        return 200
    else:
        return 404

@api.route('/tokens')
@auth.login_required
def get_auth_token():
    token = g.current_user.generate_auth_token()
    return jsonify({'token':token})


