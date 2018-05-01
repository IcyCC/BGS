from flask import Blueprint

accuchek_blueprint = Blueprint('accuchek', __name__)

from . import accucheks
