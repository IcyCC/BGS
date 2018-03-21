import os
import json

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')or 'hard to guess string'
    PATIENTS_PRE_PAGE = 20
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # some about net

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