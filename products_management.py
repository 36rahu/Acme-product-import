__date__ = '28/08/19'
__author__ = 'Rahul K P'

from threading import Thread
from datetime import datetime

from app import db
from models import Products
from webhook_manager import WebhookManager
from constants import EDIT_WEBHOOK_EVENT

webhook_manager = WebhookManager()

def add_product(product_dict):
    """Method to add product to the model.

    It's create a product if the sku not exits in the database. Else it 
    will update the exitsing one. After the successfull create / update
    function will trigger a webhook call.

    Args:
        product_dict (dict): It's a dictionary with all products info.

    Returns:
        Returns a dictionary with status and message.
    """
    try:
        product = Products.query.filter(Products.sku == product_dict['sku']).first()
        if product:
            product.name = product_dict['name']
            product.description = product_dict['description']
            product.status = product_dict['status']
            msg = 'Product updated'
            event_name = EDIT_WEBHOOK_EVENT
        else:
            product = Products(sku=product_dict['sku'],
                                name=product_dict['name'],
                                description=product_dict['description'],
                                status=product_dict['status'])
            msg = 'Product created'
            event_name = ADD_WEBHOOK_EVENT
        db.session.add(product)
        db.session.commit()
        db.session.flush()
        payload = {'product': {'name': product_dict['name'],
                                    'description': product_dict['description'],
                                    'sku': product_dict['sku'],
                                    'status': product_dict['status'],
                                    'created_date': product.created_date.strftime('%d-%m-%Y %H-%M-%s')},
                        'event_time': datetime.now().strftime('%d-%m-%Y %H-%M-%s'),
                        'event_name': 'Update Product'
                        }
        # Trigger webhooks
        thread = Thread(target = webhook_manager.triger_all_webhooks, args = (event_name, payload))
        thread.start()
        return {'status': 'SUCCESS', 'msg': msg}
    except Exception as error:
        print(str(error))
        return {'status': 'FAILED', 'msg': 'Could not create product'}

def delete_all_products():
    """Method to delete all products in the products table.

    Aftser the successfull deletion function will trigger a webhook call.

    Returns:
        Returns a dictionary with status and message.
    """
    try:
        num_rows_deleted = db.session.query(Products).delete()
        db.session.commit()
        # Trigger webhooks
        payload = {'event_time': datetime.now().strftime('%d-%m-%Y %H-%M-%s'),
                    'event_name': 'Deleted all product'
                    }
        thread = Thread(target = webhook_manager.triger_all_webhooks, args = (DELETE_WEBHOOK_EVENT, payload))
        thread.start()
        return {'status': 'SUCCESS', 'msg':'All products deleted successfully'}
    except:
        db.session.rollback()
        return {'status': 'SUCCESS', 'msg':'Products deletion failed'}
