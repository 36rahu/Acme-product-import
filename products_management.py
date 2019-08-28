__date__ = '28/08/19'
__author__ = 'Rahul K P'

from app import db
from models import Products

def add_product(product_dict):
    try:
        product = Products.query.filter(Products.sku == product_dict['sku']).first()
        if product:
            product.name = product_dict['name']
            product.description = product_dict['description']
            product.status = product_dict['status']
            msg = 'Existing product updated'
        else:
            product = Products(sku=product_dict['sku'],
                                name=product_dict['name'],
                                description=product_dict['description'],
                                status=product_dict['status'])
            msg = 'Product created'
        db.session.add(product)
        db.session.commit()
        db.session.flush()
        return {'status': 'SUCCESS', 'msg': msg}
    except Exception as error:
        print(str(error))
        return {'status': 'FAILED', 'msg': 'Could not create product'}
