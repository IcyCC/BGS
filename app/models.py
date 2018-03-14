from . import db
from flask import url_for, g, current_app, jsonify
from sqlalchemy.exc import OperationalError,IntegrityError
import os
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin,current_user
from app import login_manager

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
            'url':url_for('api.get_operator', id = self.id),
            'hospital':self.hospital,
            'office':self.office,
            'lesion':self.lesion,
            'operator_name':self.operator_name
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
    doctor_id = db.Column(db.Integer)

    @property
    def bed(self):
        bed = Bed.query.join(Patient, Patient.id_number == Bed.id_number).filter(Patient.patient_id == self.patient_id).first()
        return bed

    @property
    def doctor(self):
        doctor = Operator.query.filter(Operator.id == self.doctor_id).first()
        return doctor

    @property
    def datas(self):
        datas = Data.query.join(Patient, Patient.id_number == Data.id_number).filter(Patient.patient_id == self.patient_id).filter(Data.hidden != True).order_by(Data.date.desc(), Data.time.desc())
        return datas

    @staticmethod
    def from_json(json_post):
        patient = Patient()
        for k in json_post:
            if hasattr(patient, k):
                setattr(patient, k, json_post[k])
        operator_name = json_post['doctor']
        doctor = Operator.query.filter(Operator.operator_name == operator_name).first()
        doctor_id = doctor.id
        patient.doctor_id = doctor_id
        return patient

    def to_json(self):
        json_patient = {
            'url': url_for('api.get_patient', id=self.patient_id),
            'patient_name':self.patient_name,
            'sex':self.sex,
            'tel':self.tel,
            'age':self.age,
            'doctor_id':self.doctor_id,
            'id_number':self.id_number,
            'datas':url_for('api.get_patient_datas', id = self.patient_id)
        }
        return json_patient

class Data(db.Model):
    __tablename__ = 'datas'
    data_id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(32), nullable=False)
    id_number = db.Column(db.String(32))
    time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    glucose = db.Column(db.Float, nullable=False)
    hidden = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def patient(self):
        patient = Patient.query.join(Data, Data.id_number == Patient.id_number).filter(Data.data_id == self.data_id).first()
        return patient

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
            'url':url_for('api.get_data', id = self.data_id),
            'patient':url_for('api.get_patient', id = self.patient.patient_id),
            'sn':self.sn,
            'id_number':self.id_number,
            'time':str(self.time),
            'date':str(self.date),
            'glucose':self.glucose
        }
        return json_data

class Accuchek(db.Model):
    __tablename__ = 'accucheks'
    accuchek_id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(24), nullable=True, unique=True)
    bed_id = db.Column(db.Integer)

    @property
    def bed(self):
        bed = Bed.query.join(Accuchek, Accuchek.sn == Bed.sn).filter(Accuchek.accuchek_id == self.accuchek_id).first()
        return bed

    @property
    def datas(self):
        datas = Data.query.join(Accuchek, Accuchek.sn == Data.sn).filter(Accuchek.accuchek_id == self.accuchek_id).order_by(Data.date.desc(), Data.time.desc()).filter(Data.hidden!=True)
        return datas

    def to_json(self):
        json_accuchek = {
            'url':url_for('api.get_accuchek', id = self.accuchek_id),
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
        patient = Patient.query.join(Bed, Bed.id_number == Patient.id_number).filter(Bed.bed_id == self.bed_id).first()
        return patient

    @property
    def datas(self):
        patient = self.patient
        datas = patient.datas
        return datas

    @property
    def accuchek(self):
        accuchek = Accuchek.query.join(Bed, Bed.sn == Accuchek.sn).filter(Bed.bed_id == self.bed_id).first()
        return accuchek

    @property
    def current_datas(self):
        current_datas = self.datas.order_by(Data.date.desc(), Data.time.desc()).limit(10)
        return current_datas

    @property
    def bed_historys(self):
        bed_historys = BedHistory.query.join(Bed, Bed.bed_id == BedHistory.bed_id).filter(Bed.bed_id == self.bed_id).order_by(BedHistory.date.desc(), BedHistory.time.desc())
        return bed_historys

    def bed_information(self):
        patient = self.patient
        json_bed_information = {
            'url':url_for('api.get_bed', id=self.bed_id),
            'sn':self.sn,
            'sex': patient.sex,
            'tel': patient.tel,
            'age': patient.age,
            'patient_name':patient.patient_name,
            'doctor_id': patient.doctor_id,
            'id_number':patient.id_number,
            'current_datas':[current_data.to_json() for current_data in self.current_datas]
        }
        return json_bed_information

    def to_json(self):
        json_bed = {
            'url':url_for('api.get_bed', id = self.bed_id),
            'id_number': self.id_number,
            'sn': self.sn
        }
        return json_bed

    def to_full_information(self):
        patient_name = ''
        tel = ''
        sex = ''
        age = ''
        operator_name = ''
        datas = []

        if self.id_number is not None:
            patient = Patient.query.filter(Patient.id_number == self.id_number).first()
            patient_name = patient.patient_name
            tel = patient.tel
            sex = patient.sex
            age = patient.age
            operator_name = patient.doctor.operator_name
            current_datas = patient.datas.limit(10)
            datas = [data.to_json() for data in current_datas]

        json_bed = {
            'url': url_for('api.get_bed', id=self.bed_id),
            'id_number': self.id_number,
            'sn': self.sn,
            'bed_id': self.bed_id,
            'patient_name': patient_name,
            'tel': tel,
            'sex': sex,
            'age': age,
            'doctor': operator_name,
            'datas': datas
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
        bed = Bed.query.join(BedHistory, BedHistory.bed_id == Bed.bed_id).filter(BedHistory.history_id == self.history_id).first()
        return bed

    @property
    def patient(self):
        patient = Patient.query.join(BedHistory, BedHistory.id_number == Patient.id_number).filter(BedHistory.history_id == self.history_id).first()
        return patient

    @property
    def accuchek(self):
        accuchek = Accuchek.query.join(BedHistory, BedHistory.sn == Accuchek.sn).filter(BedHistory.history_id == self.history_id).first()
        return accuchek

    def to_json(self):
        json_history = {
            'url':url_for('api.get_history', id = self.history_id),
            'bed_id':self.bed_id,
            'time':str(self.time),
            'date':str(self.date),
            'sn':self.sn,
            'id_number':self.id_number
        }
        return json_history

@login_manager.user_loader
def load_user(id):
    return Operator.query.get(int(id))


