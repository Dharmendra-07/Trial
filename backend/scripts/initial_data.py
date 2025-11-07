from ..app import app
from ..models import db
from flask_security.datastore import SQLAlchemyUserDatastore

with app.app_context():
  datastore : SQLAlchemyUserDatastore = app.datastore

  admin_role = datastore.find_or_create_role('admin', description = 'super user')
  manager_role = datastore.find_or_create_role('manager', description = 'handles and manges store')
  customer_role = datastore.find_or_create_role('customer', description = 'buys items from store')
  
  try:
    db.session.commit()
  except:
    db.session.rollback()