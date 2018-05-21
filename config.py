import os
import json
import psutil

basedir = os.path.abspath(os.path.dirname(__file__))

def get_netcard():
    """获取网卡名称和ip地址

    """
    netcard_info = []
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and not item[1] == '127.0.0.1':
                netcard_info.append((k, item[1]))
    return netcard_info

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')or 'hard to guess string'
    PATIENTS_PRE_PAGE = 20
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    THREADED = True
    MAIL_SERVER = 'smtp.qq.com',
    MAIL_PROT = 25,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = "1468767640@qq.com",
    MAIL_PASSWORD = "ldundwdlgoopgdgi",
    MAIL_DEBUG = True
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql://root:wshwoaini@localhost:3306/test_dev?charset=utf8'
    SQLALCHEMY_BINDS = {
        'first_dev': 'mysql://root:wshwoaini@localhost:3306/first_dev?charset=utf8',
    }

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'mysql://root:wshwoaini@localhost:3306/test_dev?charset=utf8'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:wshwoaini@localhost:3306/test_dev?charset=utf8'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}