from . import db
from flask import url_for, g, current_app
import os
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Operator(db.Model):
    __tablename__ = 'operators'
    operator_id = db.Column(db.Integer, primary_key=True)
    operator_name = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    hospital = db.Column(db.String(128), nullable=False)
    office = db.Column(db.String(128), nullable=False)
    lesion = db.Column(db.String(128))
    tel = db.Column(db.String(16), nullable=False, unique=True)
    mail = db.Column(db.String(64), unique=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def patients(self):
        patients = Patient.query.join(Operator, Operator.operator_id == Patient.doctor_id).filter(Operator.operator_id == self.operator_id)
        return patients

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'operator_id':self.operator_id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return None
        operator = Operator.query.get_or_404(data['operator_id'])
        return operator

    @staticmethod
    def from_json(json_post):
        hospital = json_post['hospital']
        office = json_post['office']
        lesion = json_post['lesion']
        operator_name = json_post['operator_name']
        tel = json_post['tel']
        mail = json_post['mail']
        password = json_post['password']
        operator = Operator(hospital = hospital, office = office, operator_name = operator_name, lesion = lesion, tel = tel, mail = mail)
        operator.password = password
        return operator

    def to_json(self):
        json_operator = {
            'url':url_for('api.get_operator', id = self.operator_id),
            'hospital':self.hospital,
            'office':self.office,
            'lesion':self.lesion,
            'operator_name':self.operator_name
        }
        return json_operator

class Patient(db.Model):
    __tablename__ = 'patients'
    patient_id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(64), nullable=False)
    sex = db.Column(db.String(64), nullable=False)
    tel = db.Column(db.String(16), nullable=False)
    id_number = db.Column(db.String(32), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)

    @property
    def bed(self):
        bed = Bed.query.join(Patient, Patient.id_number == Bed.id_number).filter(Patient.patient_id == self.patient_id).first()
        return bed

    @property
    def doctor(self):
        doctor = Operator.query.filter(Operator.operator_id == self.doctor_id).first()
        return doctor

    @property
    def datas(self):
        datas = Data.query.join(Patient, Patient.id_number == Data.id_number).filter(Patient.patient_id == self.patient_id).filter(Data.hidden != True)
        return datas

    @staticmethod
    def from_json(json_post):
        patient = Patient()
        for k in json_post:
            if hasattr(patient, k):
                setattr(patient, k, json_post[k])
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
    time = db.Column(db.Time, nullable=True)
    date = db.Column(db.Date, nullable=True)
    glucose = db.Column(db.Float, nullable=True)
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
        datas = Data.query.join(Accuchek, Accuchek.sn == Data.sn).filter(Accuchek.accuchek_id == self.accuchek_id)
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
        current_datas = self.datas.order_by(Data.data_id.desc()).limit(10)
        return current_datas

    @property
    def bed_historys(self):
        bed_historys = BedHistory.query.join(Bed, Bed.bed_id == BedHistory.bed_id).filter(Bed.bed_id == self.bed_id)
        return bed_historys

    def bed_information(self):
        patient = self.patient
        json_bed_information = {
            'id':self.bed_id,
            'sn':self.sn,
            'sex': patient.sex,
            'tel': patient.tel,
            'age': patient.age,
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

class BedHistory(db.Model):
    __tablename__ = 'bedhistory'
    history_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Time, nullable=True)
    date = db.Column(db.Date, nullable=True)
    bed_id = db.Column(db.Integer)
    sn = db.Column(db.String(32))
    id_number = db.Column(db.String(64))

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


