from . import db
from flask import url_for, g, current_app
import os
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Operator(db.Model):
    __tablename__ = 'operators'
    id = db.Column(db.Integer, primary_key=True)
    operator_name = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    hospital = db.Column(db.String(128), nullable=False)
    office = db.Column(db.String(128), nullable=False)
    lesion = db.Column(db.String(128))
    tel = db.Column(db.String(16), nullable=False, unique=True)
    mail = db.Column(db.String(16), unique=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'id':self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return None
        operator = Operator.query.get(data['id'])
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
            'url':url_for('api.get_operator', id = self.id),
            'hospital':self.hospital,
            'office':self.office,
            'lesion':self.lesion,
            'operator_name':self.operator_name
        }
        return json_operator

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(64), nullable=False)
    sex = db.Column(db.String(64), nullable=False)
    tel = db.Column(db.String(16), nullable=False)
    id_number = db.Column(db.String(32), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    doctor_name = db.Column(db.String(64), nullable=False)

    @property
    def bed(self):
        bed = Bed.query.join(Patient, Patient.patient_name == Bed.patient_name).filter_by(Patient.patient_name == self.patient_name).first()
        return bed

    @property
    def datas(self):
        datas = Data.query.join(Patient, Patient.patient_name == Data.patient_name).filter_by(Patient.patient_name == self.patient_name)
        return datas

    def to_json_data(self):
        json_patient = {
            'patient_name':self.patient_name,
            'sex':self.sex,
            'tel':self.tel,
            'age':self.age,
            'doctor_name':self.doctor_name,
            'id_number':self.id_number,
            'datas':[data.to_json() for data in self.datas]
        }
        return json_patient

    @staticmethod
    def from_json(json_post):
        patient_name = json_post['patient_name']
        sex = json_post['sex']
        tel = json_post['tel']
        age = json_post['age']
        doctor_name = json_post['doctor_name']
        id_number = json_post['id_number']
        patient = Patient(patient_name = patient_name, sex = sex, tel = tel, age = age, doctor_name = doctor_name, id_number=id_number)
        return patient

    def to_json(self):
        json_patient = {
            'url':url_for('api.get_patient', id = self.id),
            'patient_name':self.patient_name,
            'sex':self.sex,
            'tel':self.tel,
            'age':self.age,
            'doctor_name':self.doctor_name,
            'id_number':self.id_number
        }
        return json_patient

class Data(db.Model):
    __tablename__ = 'datas'
    id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(32), nullable=False)
    patient_name = db.Column(db.String(64), nullable=False)
    time = db.Column(db.Time, nullable=True)
    date = db.Column(db.Date, nullable=True)
    glucose = db.Column(db.Float, nullable=True)
    hidden = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def patient(self):
        patient = Patient.query.join(Data, Data.patient_name == Patient.patient_name).filter_by(Patient.patient_name == self.patient_name).first()
        return patient

    @staticmethod
    def from_json(json_post):
        patient_name = json_post['patient_name']
        time = json_post['time']
        date = json_post['date']
        glucose = json_post['glucose']
        data = Data(patient_name=patient_name, time = time, date = date, glucose = glucose)
        return data

    def to_json(self):
        json_data = {
            'url':url_for('api.get_data', id = self.id),
            'sn':self.sn,
            'patient_name':self.patient_name,
            'time':self.time,
            'date':self.date,
            'glucose':self.glucose
        }
        return json_data

class Accuchek(db.Model):
    __tablename__ = 'accucheks'
    id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(24), nullable=True)
    bed_number = db.Column(db.Integer)

    @property
    def bed(self):
        bed = Bed.query.join(Accuchek, Accuchek.sn == Bed.sn).filter_by(Accuchek.id == self.id).first()
        return bed


class Bed(db.Model):
    __tablename__ = 'beds'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(64))
    sn = db.Column(db.String(24))

    @property
    def patient(self):
        patient = Patient.query.join(Bed, Bed.patient_name == Patient.patient_name).filter_by(Bed.id == self.id).first()
        return patient

    @property
    def data(self):
        datas = Data.query.join(Bed, Bed.patient_name == Data.patient_name).filter_by(Data.patient_name == self.patient_name).filter_by(Data.hidden == False)
        return datas

    @property
    def accuchek(self):
        accuchek = Accuchek.query.join(Bed, Bed.sn == Accuchek.sn).filter_by(Bed.id == self.id).first()
        return accuchek

    def current_datas(self):
        current_datas = self.data.order_by(Data.id.desc()).limit(10)
        return current_datas

    def all_datas(self):
        all_datas = self.data
        return all_datas

    def bed_information(self):
        patient = self.patient
        json_bed_information = {
            'id':self.id,
            'patient_name': self.patient_name,
            'sn':self.sn,
            'sex': patient.sex,
            'tel': patient.tel,
            'age': patient.age,
            'doctor_name': patient.doctor_name,
            'id_number':patient.id_number,
            'current_datas':[current_data.to_json() for current_data in self.current_datas()]
        }
        return json_bed_information

    def to_json(self):
        json_bed = {
            'id': self.id,
            'patient_name': self.patient_name,
            'sn': self.sn
        }
        return json_bed


