__date__ = '26/08/19'
__author__ = 'Rahul K P'

import enum
import datetime

from app import db
from constants import *

class StatusEnum(enum.Enum):
    ACTIVE = ACTIVE
    INACTIVE = INACTIVE

class ModelBaseClass:
    """Base class use for all models."""
    status = db.Column(db.Enum(StatusEnum), nullable=False)
    created_by = db.Column(db.VARCHAR(length=64), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_by = db.Column(db.VARCHAR(length=64), nullable=True)
    updated_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Products(ModelBaseClass, db.Model):
    """Products model"""
    __tablename__ = 'products'

    sku = db.Column(db.VARCHAR(length=64), nullable=False, primary_key=True)
    name = db.Column(db.VARCHAR(length=64), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Webhooks(db.Model):
    """Webhook Model"""
    __tablename__ = 'webhooks'

    id = db.Column(db.INTEGER, nullable=False, primary_key=True)
    event = db.Column(db.VARCHAR(length=64), nullable=False)
    endpoint = db.Column(db.VARCHAR(length=64), nullable=False)
    method = db.Column(db.VARCHAR(length=64), nullable=False)
    host = db.Column(db.VARCHAR(length=100), nullable=False)
    extra_paylod = db.Column(db.JSON, nullable=True)
