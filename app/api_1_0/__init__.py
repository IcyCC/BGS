from flask import Blueprint

api = Blueprint('api', __name__)

from . import operators, authentication, accuchek, patients, datas, beds