#-*- coding=utf-8 -*-
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail
from datetime import timedelta
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'None'
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.config.update(
        MAIL_SERVER='smtp.qq.com',
        MAIL_PROT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
        MAIL_USERNAME="1468767640@qq.com",
        MAIL_PASSWORD="uhieluellzqwhaea",
        MAIL_DEBUG=True
    )

    login_manager.init_app(app)
    login_manager.remember_cookie_duration = timedelta(days=1000)



    db.init_app(app)
    mail.init_app(app)

    app.template_folder='/home/zhandong/PycharmProjects/accu_chek/templates'

    from .gencode import gencode
    app.register_blueprint(gencode, url_prefix='/gencode')

    from .accuchek import accuchek
    app.register_blueprint(accuchek, url_prefix='/accuchek')

    from .bed import bed
    app.register_blueprint(bed, url_prefix='/bed')

    from .operator import operator
    app.register_blueprint(operator, url_prefix='/operator')

    from .data import data
    app.register_blueprint(data, url_prefix='/data')

    from .patient import patient
    app.register_blueprint(patient, url_prefix='/patient')

    CORS(app, supports_credentials=True)

    return app
