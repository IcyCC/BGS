from flask import Blueprint

bed_blueprint = Blueprint('bed', __name__)

from . import beds, bedhistory
