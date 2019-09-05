from time import sleep
import os
from os import path
import boto3
import json
import urllib.request
from flask import Flask, flash, request, redirect, render_template, Blueprint, jsonify
from werkzeug.utils import secure_filename
from flask_sse import sse
from app import app, db
from celery_task import insert_value_in_model
import pandas as pd
import numpy as np
from io import StringIO

from constants import EDIT_LINK
from utils import allowed_file
from models import Products
from products_management import add_product
from webhook_manager import WebhookManager

views = Blueprint('views', __name__)
webhook_manager = WebhookManager()

@views.route('/')
def upload_form():
    return render_template('upload.html')

@views.route('/upload/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file_url = request.form["input_file"]
        # Celery task start
        task = insert_value_in_model.apply_async(args=[file_url])
        return redirect('/')

@views.route('/products_list/')
def get_products_list():
    products = [{'sku': prod.sku,
                'name': prod.name,
                'description': prod.description,
                'status': prod.status.name,
                'edit_link': EDIT_LINK.format(prod.sku)} 
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

@views.route('/product/edit/<sku>/', methods=['POST', 'GET'])
def edit_products(sku=None):
    if request.method == 'POST':
        res = add_product(request.form)
        flash(res.get('msg'))
    product = Products.query.filter(Products.sku == sku).first()
    if product:
        product_data = {'sku': product.sku,
                        'name': product.name,
                        'description': product.description,
                        'status': product.status.name
                        }
        return render_template('product_edit.html', data=product_data)
    flash('Products not exit')
    return render_template('product_edit.html')

@views.route('/webhook/add/', methods=['POST', 'GET'])
def add_webhook():
    if request.method == 'POST':
        webhook_manager.create_webhook(request.form)
        flash('webhook creeated')
    return render_template('webhook_add.html')

@views.route('/sign_s3/')
def sign_s3():
    S3_BUCKET = os.environ.get('S3_BUCKET')
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    s3 = boto3.client('s3')
    presigned_post = s3.generate_presigned_post(
        Bucket = S3_BUCKET,
        Key = file_name,
        Fields = {"acl": "public-read", "Content-Type": file_type},
        Conditions = [
            {"acl": "public-read"},
            {"Content-Type": file_type}
            ],
        ExpiresIn = 3600
    )
    print(presigned_post)
    return json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
        })


