from flask import Blueprint

accuchek_blueprint = Blueprint('accuchek_blueprint', __name__)

from . import accucheks
