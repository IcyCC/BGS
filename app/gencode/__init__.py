from flask import Blueprint

gencode_blueprint = Blueprint('gencode_blueprint', __name__)

from . import gen_code