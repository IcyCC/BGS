#-*- coding=utf-8 -*-
from flask import Flask,url_for, redirect
from flask_script import Manager, Shell
from app import create_app, db
from app.models import Operator
import os
from flask_migrate import Migrate, upgrade, MigrateCommand
from flask_cors import CORS
import pymysql
import json

pymysql.install_as_MySQLdb()
from app.fake import operators, man_patients, woman_patients, accucheks, datas

app = create_app(os.getenv('FLASK_CONFIG')or 'default')
app._static_folder = os.path.abspath('./static')

with open("config.json",'r+') as f:
    app.custom_net_setting = json.load(f).get('net')
    print(app.custom_net_setting)


manager = Manager(app)
migrate = Migrate(app, db)
CORS(app)

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
    operators()
    man_patients()
    woman_patients()
    accucheks()
    datas()

def make_shell_context():
    return dict(app=app, db=db, create_all= create_all, Operator=Operator)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@app.route('/doc', methods=['GET'])
def doc_ser():
    return redirect(url_for("static", filename="apidoc/index.html", _external=True))

if __name__ == '__main__':
    app.run()
