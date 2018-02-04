from . import api
import os
from .. import db
from flask import request, jsonify, g, url_for
from ..models import Patient, Operator, Data, Bed, Accuchek
from .authentication import auth
import datetime

@api.route('/datas', methods = ['POST'])
def new_data():
    glucose = request.json['glucose']
    sn = request.json['sn']
    bed = Accuchek.query.filter_by(Accuchek.sn == sn).first()
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time()
    data = Data(date=date, time=time, glucose=glucose, sn=sn)
    db.session.add(data)
    db.session.commit()
    return 200