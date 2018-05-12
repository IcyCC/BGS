from . import db
from flask import url_for, g, current_app, jsonify
from sqlalchemy.exc import OperationalError,IntegrityError
import os
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin,current_user
from app import login_manager
from datetime import datetime

class Operator(db.Model, UserMixin):
    __tablename__ = 'operators'
    id = db.Column(db.Integer, primary_key=True)
    operator_name = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    hospital = db.Column(db.String(128), nullable=False)
    office = db.Column(db.String(128), nullable=False)
    lesion = db.Column(db.String(128))
    tel = db.Column(db.String(16), nullable=False, unique=True)
    mail = db.Column(db.String(64))
    active = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def patients(self):
        patients = Patient.query.join(Operator, Operator.id == Patient.doctor_id).filter(Operator.id == self.id)
        return patients

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def from_json(json_post):
        operator = Operator()
        for k in json_post:
            if hasattr(operator, k):
                try:
                    setattr(operator, k, json_post[k])
                except IntegrityError as e:
                    return jsonify({
                        'status': 'fail',
                        'reason': str(e)
                    })
        operator.password = json_post['password']
        return operator

    def to_json(self):
        json_operator = {
            'operator_id':self.id,
            'hospital':self.hospital,
            'office':self.office,
            'lesion':self.lesion,
            'operator_name':self.operator_name,
            'active':self.active
        }
        return json_operator
login_manager.anonymous_user = AnonymousUserMixin
class Patient(db.Model):
    __tablename__ = 'patients'
    patient_id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(64))
    sex = db.Column(db.String(64))
    tel = db.Column(db.String(16))
    id_number = db.Column(db.String(32), unique=True)
    age = db.Column(db.Integer)
    doctor_name = db.Column(db.String(32))

    @property
    def bed(self):
        try:
            bed = Bed.query.join(Patient, Patient.id_number == Bed.id_number).filter(Patient.patient_id == self.patient_id).first()
            return bed
        except:
            return None


    @property
    def datas(self):
        try:
            datas = Data.query.join(Patient, Patient.id_number == Data.id_number).filter(Patient.patient_id == self.patient_id).filter(Data.hidden != True).order_by(Data.date.desc(), Data.time.desc())
            return datas
        except:
            return Data.query.filter(Data.data_id == -1)

    @staticmethod
    def from_json(json_post):
        patient = Patient()
        for k in json_post:
            if hasattr(patient, k):
                setattr(patient, k, json_post[k])
        return patient

    def to_json(self):
        json_patient = {
            'patient_id': self.patient_id,
            'patient_name':self.patient_name,
            'sex':self.sex,
            'tel':self.tel,
            'age':self.age,
            'doctor':self.doctor_name,
            'id_number':self.id_number,
            'datas_url': url_for('patient_blueprint.get_patient_datas', id=self.patient_id)
        }
        return json_patient

class Data(db.Model):
    __tablename__ = 'datas'
    data_id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(32), nullable=False)
    id_number = db.Column(db.String(32))
    time = db.Column(db.Time, nullable=False, default=datetime.utcnow().time())
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    glucose = db.Column(db.Float, nullable=False)
    hidden = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def patient(self):
        try:
            patient = Patient.query.join(Data, Data.id_number == Patient.id_number).filter(Data.data_id == self.data_id).first()
            return patient
        except:
            return None

    @staticmethod
    def from_json(json_post):
        id_number = json_post['id_number']
        time = json_post['time']
        date = json_post['date']
        glucose = json_post['glucose']
        data = Data(id_number=id_number, time = time, date = date, glucose = glucose)
        return data

    def to_json(self):
        json_data = {
            'data_id':self.data_id,
            'patient':self.patient.to_json() if self.patient is not None else None,
            'sn':self.sn,
            'id_number':self.id_number,
            'time':str(self.time)[0:5],
            'date':str(self.date),
            'glucose':self.glucose
        }
        return json_data

    def to_guard_json(self):
        json_data = {
            'data_id': self.data_id,
            'sn': self.sn,
            'id_number': self.id_number,
            'time': str(self.time)[0:5],
            'date': str(self.date),
            'glucose': self.glucose
        }
        return json_data

    def to_full_json(self):
        patient = self.patient
        json_data = {
            'patient_name': patient.patient_name if patient is not None else None,
            'age': patient.age if patient is not None else None,
            'tel': patient.tel if patient is not None else None,
            'doctor': patient.doctor_name if patient is not None else None,
            'id_number': self.id_number,
            'date': str(self.date),
            'sn':self.sn,
            'time': str(self.time)[0:5],
            'glucose': self.glucose,
            'sex': patient.sex if patient is not None else None,
            'data_id':self.data_id
        }
        return json_data

class Accuchek(db.Model):
    __tablename__ = 'accucheks'
    accuchek_id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(24), nullable=True, unique=True)
    bed_id = db.Column(db.Integer)

    @property
    def bed(self):
        try:
            bed = Bed.query.join(Accuchek, Accuchek.sn == Bed.sn).filter(Accuchek.accuchek_id == self.accuchek_id).first()
            return bed
        except:
            return None

    @property
    def datas(self):
        try:
            datas = Data.query.join(Accuchek, Accuchek.sn == Data.sn).filter(Accuchek.accuchek_id == self.accuchek_id).order_by(Data.date.desc(), Data.time.desc()).filter(Data.hidden!=True)
            return datas
        except:
            return Data.query.filter(Data.data_id == -1).order_by(Data.date.desc(), Data.time.desc()).filter(Data.hidden!=True)

    def to_json(self):
        json_accuchek = {
            'accuchek_id':self.accuchek_id,
            'sn':self.sn,
            'bed_id':self.bed_id
        }
        return json_accuchek


class Bed(db.Model):
    __tablename__ = 'beds'
    bed_id = db.Column(db.Integer, primary_key=True)
    id_number = db.Column(db.String(32))
    sn = db.Column(db.String(24))

    @property
    def patient(self):
        try:
            patient = Patient.query.join(Bed, Bed.id_number == Patient.id_number).filter(Bed.bed_id == self.bed_id).first()
            return patient
        except:
            return Patient.query.filter(Patient.patient_id == -1).first()

    @property
    def datas(self):
        try:
            patient = self.patient
            datas = patient.datas
            return datas
        except:
            datas = Data.query.filter(Data.data_id == -1)
            return datas

    @property
    def accuchek(self):
        try:
            accuchek = Accuchek.query.join(Bed, Bed.sn == Accuchek.sn).filter(Bed.bed_id == self.bed_id).first()
            return accuchek
        except:
            return Accuchek.query.filter(Accuchek.accuchek_id == -1).first()

    @property
    def current_datas(self):
        try:
            current_datas = self.datas.order_by(Data.date.desc(), Data.time.desc()).limit(10)
            return current_datas
        except:
            return Data.query.filter(Data.data_id == -1).order_by(Data.date.desc(), Data.time.desc()).limit(10)

    @property
    def bed_historys(self):
        try:
            bed_historys = BedHistory.query.join(Bed, Bed.bed_id == BedHistory.bed_id).filter(Bed.bed_id == self.bed_id).order_by(BedHistory.date.desc(), BedHistory.time.desc())
            return bed_historys
        except:
            return BedHistory.query.filter(BedHistory.history_id ==-1)

    def bed_current_data(self):
        #返回最近十组数据
        patient = self.patient
        json_bed_information = {
            'bed_id':self.bed_id,
            'sn':self.sn,
            'sex': patient.sex if patient is not None else None,
            'tel': patient.tel if patient is not None else None,
            'age': patient.age if patient is not None else None,
            'patient_name':patient.patient_name if patient is not None else None,
            'doctor': patient.doctor_name if patient is not None else None,
            'id_number':patient.id_number if patient is not None else None,
            'current_datas':[current_data.to_json() for current_data in self.current_datas]
        }
        return json_bed_information

    def bed_full_data(self):
        #返回所有数据
        patient = self.patient
        json_bed_information = {
            'bed_id':self.bed_id,
            'sn':self.sn,
            'sex': patient.sex if patient is not None else None,
            'tel': patient.tel if patient is not None else None,
            'age': patient.age if patient is not None else None,
            'patient_name':patient.patient_name if patient is not None else None,
            'doctor': patient.doctor_name if patient is not None else None,
            'id_number':patient.id_number if patient is not None else None,
            'datas':[current_data.to_json() for current_data in self.datas]
        }
        return json_bed_information

    def to_json(self):
        json_bed = {
            'bed_id':self.bed_id,
            'id_number': self.id_number,
            'sn': self.sn
        }
        return json_bed

class BedHistory(db.Model):
    __tablename__ = 'bedhistory'
    history_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Time, nullable=True)
    date = db.Column(db.Date, nullable=True)
    bed_id = db.Column(db.Integer, nullable=True)
    sn = db.Column(db.String(32), nullable=True)
    id_number = db.Column(db.String(64), nullable=True)

    @property
    def bed(self):
        try:
            bed = Bed.query.join(BedHistory, BedHistory.bed_id == Bed.bed_id).filter(BedHistory.history_id == self.history_id).first()
            return bed
        except:
            return None

    @property
    def patient(self):
        try:
            patient = Patient.query.join(BedHistory, BedHistory.id_number == Patient.id_number).filter(BedHistory.history_id == self.history_id).first()
            return patient
        except:
            return None

    @property
    def accuchek(self):
        try:
            accuchek = Accuchek.query.join(BedHistory, BedHistory.sn == Accuchek.sn).filter(BedHistory.history_id == self.history_id).first()
            return accuchek
        except:
            return None

    def to_json(self):
        json_history = {
            'history_id':self.history_id,
            'bed_id':self.bed_id,
            'time':str(self.time)[0:5],
            'date':str(self.date),
            'sn':self.sn,
            'id_number':self.id_number
        }
        return json_history

class SpareData(db.Model):
    __tablename__ = 'guarddatas'
    data_id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(32), nullable=False)
    id_number = db.Column(db.String(32))
    patient_name = db.Column(db.String(32))
    sex = db.Column(db.String(4))
    age = db.Column(db.Integer)
    tel = db.Column(db.String(32))
    doctor = db.Column(db.String(64))
    time = db.Column(db.Time, nullable=False, default=datetime.utcnow().time())
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    glucose = db.Column(db.Float, nullable=False)
    hidden = db.Column(db.Boolean, nullable=False, default=False)

    def to_full_json(self):
        json_data = {
            'data_id': self.data_id,
            'patient_name': self.patient_name,
            'age': self.age,
            'sex':self.sex,
            'tel': self.tel,
            'sn': self.sn,
            'doctor': self.doctor,
            'id_number': self.id_number,
            'date': str(self.date),
            'time': str(self.time)[0:5],
            'glucose': self.glucose

        }
        return json_data

@login_manager.user_loader
def load_user(id):
    print('load_user')
    return Operator.query.get(int(id))


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.split(' ')[1]
        # print(api_key)
        obj = jwtDecoding(api_key)
        # print(obj)
        if obj:
            user = Operator.query.get(int(obj['id']))
            return user
        else:
            return None


from app.operator.authentication import jwtDecoding, jwtEncoding