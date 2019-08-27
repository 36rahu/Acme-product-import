__date__ = '26/08/19'
__author__ = 'Rahul K P'

from time import sleep
import os
import urllib.request
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_sse import sse
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


from utils import allowed_file
from constants import UPLOAD_FOLDER


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['REDIS_URL'] = 'redis://localhost'
app.register_blueprint(sse, url_prefix='/stream')
db = SQLAlchemy(app)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            publish_hello()
            return redirect('/')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)

def publish_hello():
    # Sample test code for publish message
    for i in range(1, 100, 10):
        sleep(1)
        sse.publish({"message": i}, type='greeting')
    return "Message sent!"


if __name__ == '__main__':
    app.run()