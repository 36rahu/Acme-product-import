from time import sleep
import os
from os import path
import urllib.request
from flask import Flask, flash, request, redirect, render_template, Blueprint, jsonify
from werkzeug.utils import secure_filename
from flask_sse import sse
from app import app, db
from celery_task import insert_value_in_model
import pandas as pd
import numpy as np

from constants import PER_PAGE
from utils import allowed_file
from models import Products
from products_management import add_product

views = Blueprint('views', __name__)

@views.route('/')
def upload_form():
    return render_template('upload.html')

@views.route('/upload/', methods=['POST'])
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
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            flash('File successfully uploaded')
            task = insert_value_in_model.apply_async(args=[file_path])
            return redirect('/')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)

@views.route('/products_list/')
def get_products_list():
    products = [{'sku': prod.sku, 'name': prod.name, 'description': prod.description, 'status': prod.status.name} 
    for prod in db.session.query(Products).all()]
    return jsonify({'data': products})

@views.route('/products/')
def get_products():
    return render_template('products.html')

@views.route('/products/delete/', methods=['GET', 'POST'])
def delete_products():
    if request.method == 'POST':
        try:
            num_rows_deleted = db.session.query(Products).delete()
            db.session.commit()
            flash('All products deleted successfully')
        except:
            db.session.rollback()
            flash('Products deletion failed')
    return render_template('products_delete.html')


@views.route('/products/add/', methods=['POST', 'GET'])
def add_products():
    if request.method == 'POST':
        res = add_product(request.form)
        flash(res.get('msg'))
    return render_template('product_add.html')

