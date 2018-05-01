from flask import Blueprint

error_blueprint = Blueprint('data', __name__)

from . import error