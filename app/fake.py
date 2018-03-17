from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import Operator, Accuchek, Bed, Data, Patient, BedHistory

def operators(count=25):
    fake = Faker(locale='zh_CN')
    i = 0
    while i < count:
        u = Operator(
            operator_name=fake.name(),
            password = 'password',
            hospital = '空军总院',
            office = '牙科',
            lesion = '无所谓',
            tel = fake.phone_number(),
            mail = fake.email()
        )
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def man_patients(count=50):
    fake = Faker(locale='zh_CN')
    i = 0
    operator_count = Operator.query.count()
    while i < count:
        o = Operator.query.offset(randint(0, operator_count-1)).first()
        p = Patient(
            patient_name=fake.name(),
            sex = "男",
            tel = fake.phone_number(),
            id_number = fake.phone_number(),
            age = randint(20, 80),
            doctor_name = fake.name()
        )
        db.session.add(p)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def woman_patients(count=50):
    fake = Faker(locale='zh_CN')
    i = 0
    operator_count = Operator.query.count()
    while i < count:
        o = Operator.query.offset(randint(0, operator_count-1)).first()
        p = Patient(
            patient_name=fake.name(),
            sex="女",
            tel=fake.phone_number(),
            id_number=fake.phone_number(),
            age=randint(20, 80),
            doctor_name=fake.name()
        )
        db.session.add(p)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def accucheks(count=70):
    fake = Faker(locale='zh_CN')
    i = 0
    p_count = Patient.query.count()
    while i <count:
        p = Patient.query.offset(randint(0, p_count - 1)).first()
        a = Accuchek(
            bed_id=randint(1, 70),
            sn = fake.phone_number()
        )
        db.session.add(a)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

        b = Bed(
            id_number = p.id_number,
            sn = a.sn
        )
        db.session.add(b)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def datas(count=1000):
    fake = Faker(locale='zh_CN')
    i=0
    a_count = Accuchek.query.count()
    p_count = Patient.query.count()
    while i<count:
        p = Patient.query.offset(randint(0, p_count-1)).first()
        a = Accuchek.query.offset(randint(0, a_count-1)).first()
        d = Data(
            sn = a.sn,
            time = fake.time(),
            date = fake.date(),
            id_number=p.id_number,
            glucose=randint(10, 20)
        )
        db.session.add(d)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def guard_datas(count=200):
    fake = Faker(locale='zh_CN')
    i = 0
    while i<count:
        d = Data(
            sn = '00000',
            time = fake.time(),
            date = fake.date(),
            glucose=randint(10,20)
        )
        db.session.add(d)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()