#-*- coding=utf-8 -*-
from flask import Flask
from flask_script import Manager, Shell
from app import create_app, db
from app.models import Operator
import os
import pymysql
pymysql.install_as_MySQLdb()

app = create_app(os.getenv('FLASK_CONFIG')or 'default')
manager = Manager(app)

def create_all():
    db.drop_all()
    db.create_all()
    hospital = "空军总院",
    office = "牙科",
    lesion = "北京",
    operator_name = "郑湛东",
    tel = "15810058975",
    mail = "1468767640",
    password = "wshwoaini"
    operator = Operator(hospital= hospital, office=office, lesion=lesion, operator_name= operator_name, tel=tel, mail=mail)
    operator.password = password
    db.session.add(operator)
    db.session.commit()

def make_shell_context():
    return dict(app=app, db=db, create_all= create_all, Operator=Operator)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
