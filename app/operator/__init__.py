from flask import Blueprint

operator_blueprint = Blueprint('operator_blueprint', __name__)

from . import operators, authentication
