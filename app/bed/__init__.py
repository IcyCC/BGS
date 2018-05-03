from flask import Blueprint

bed_blueprint = Blueprint('bed_blueprint', __name__)

from . import beds, bedhistory
