__date__ = '26/08/19'
__author__ = 'Rahul K P'

import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
import models

# Configure dtabase commands which used for DB migrations
app.config.from_object(os.environ['APP_SETTINGS'])
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()