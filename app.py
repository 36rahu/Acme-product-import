__date__ = '26/08/19'
__author__ = 'Rahul K P'

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()