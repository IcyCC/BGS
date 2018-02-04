from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for
from ..models import Patient, Operator, Data, Bed
from .authentication import auth

@api.route('/accucheks')
def accunckes():
    return