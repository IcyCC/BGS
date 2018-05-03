from flask import Blueprint

data_blueprint = Blueprint('data_blueprint', __name__)

from . import datas
