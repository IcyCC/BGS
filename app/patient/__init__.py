from flask import Blueprint

patient_blueprint = Blueprint('patient', __name__)

from . import patients