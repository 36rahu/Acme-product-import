__date__ = '26/08/19'
__author__ = 'Rahul K P'

from time import sleep
import os
import urllib.request
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_sse import sse
from celery import Celery
import pandas as pd
import numpy as np
from celery.utils.log import get_task_logger
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from constants import UPLOAD_FOLDER, SPLIT_CON

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

app.register_blueprint(sse, url_prefix='/stream')
db = SQLAlchemy(app)

