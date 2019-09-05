
from os import path
import pandas as pd
import numpy as np
from celery.utils.log import get_task_logger
from celery import Celery

from app import app, db, sse
from constants import SPLIT_CON
from models import Products

# Setup Celery
logger = get_task_logger(__name__)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def insert_value_in_model(data):
    """Method to insert products into database using celery.

    It's also send real time update to the frontend using SSE

    Args:
        data (dict): It's a dictionary created with pandas

    Returns:
        Returns 'completed'.
    """
    logger.info('celery started.....')
    with app.app_context(file_url):
        df = pd.read_csv(file_url, index_col='sku', names=['name', 'sku', 'description'], skiprows=1)
        # df = pd.read_json(data, orient='index')
        split_value = len(df) / SPLIT_CON
        sse.publish({"message": 0}, type='greeting')
        for k,g in df.groupby(np.arange(len(df))//split_value):
            for index, row in g.iterrows():
                product = Products.query.filter(Products.sku == index).first()
                if product:
                    product.name = row['name']
                    product.description = row['description']
                else:
                    product = Products(sku=index, name=row['name'], description=row['description'], status='ACTIVE')
                db.session.add(product)
            db.session.commit()
            db.session.flush()
            percent = round(((k)*split_value/float(len(df)))*100,2)
            logger.info('percent : {}'.format(percent))
            sse.publish({"message": percent}, type='greeting')
        sse.publish({"message": 100}, type='greeting')
    logger.info('celery stopped.....')
    return 'Completed'