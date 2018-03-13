#-*- coding=utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
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



    db.init_app(app)
    mail.init_app(app)

    app.template_folder='/home/zhandong/PycharmProjects/accu_chek/templates'

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    CORS(app, supports_credentials=True)

    return app
