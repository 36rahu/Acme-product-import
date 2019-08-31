
from os import path
from celery import Celery
import pandas as pd
import numpy as np
from celery.utils.log import get_task_logger

from app import app, db, sse
from constants import UPLOAD_FOLDER, SPLIT_CON
from models import Products

logger = get_task_logger(__name__)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def insert_value_in_model(filename):
    logger.info('celery started.....')
    logger.info('File path : {}'.format(filename))
    logger.info('Is exists : {}'.format(path.exists(filename)))
    df = pd.read_csv(filename, index_col='sku', names=['name', 'sku', 'description'], skiprows=1)
    split_value = len(df) / SPLIT_CON
    with app.app_context():
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
    return 'Test'