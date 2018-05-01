from flask import Blueprint

operator_blueprint = Blueprint('operator', __name__)

from . import operators, authentication
