from flask import Blueprint

gencode_blueprint = Blueprint('gencode', __name__)

from . import gen_code