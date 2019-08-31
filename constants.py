__date__ = '26/08/19'
__author__ = 'Rahul K P'

# All constants Declare here

ACTIVE = 'ACTIVE'
INACTIVE = 'INACTIVE'
ALLOWED_EXTENSIONS = set(['csv'])
UPLOAD_FOLDER = 'uploads/'
SPLIT_CON = 500
PER_PAGE = 100
EDIT_LINK = '<a href="/product/edit/{}/">Edit</a>'

EDIT_WEBHOOK_EVENT = 'edit_product'
ADD_WEBHOOK_EVENT = 'add_product'
DELETE_WEBHOOK_EVENT = 'delete_products'