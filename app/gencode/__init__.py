from flask import Blueprint

gencode = Blueprint('gencode', __name__)

from . import gen_code