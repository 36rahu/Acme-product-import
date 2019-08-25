__date__ = '26/08/19'
__author__ = 'Rahul K P'

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '57b4bb9fc9b57a242b22f140f5e102fc4b7bdc821782b3dd'
    SQLALCHEMY_DATABASE_URI = os.environ['DB_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
