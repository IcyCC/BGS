from flask import Blueprint

bed = Blueprint('bed', __name__)

from . import beds, bedhistory
