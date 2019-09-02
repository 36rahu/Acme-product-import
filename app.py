__date__ = '26/08/19'
__author__ = 'Rahul K P'

import os
import urllib.request
from flask import Flask
from flask_sse import sse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['REDIS_URL'] = os.environ['REDIS_URL']
app.config['CELERY_BROKER_URL'] = os.environ['REDIS_URL']
app.config['CELERY_RESULT_BACKEND'] = os.environ['REDIS_URL']
# Registor app
app.register_blueprint(sse, url_prefix='/stream')
# Set Datatabse
db = SQLAlchemy(app)

