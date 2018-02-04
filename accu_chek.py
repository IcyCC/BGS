#-*- coding=utf-8 -*-
from flask import Flask
from flask_script import Manager, Shell
from app import create_app, db
import os
import pymysql
pymysql.install_as_MySQLdb()

app = create_app(os.getenv('FLASK_CONFIG')or 'default')
manager = Manager(app)

def create_all():
    db.drop_all()
    db.create_all()

def make_shell_context():
    return dict(app=app, db=db, create_all= create_all)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    app.run()
