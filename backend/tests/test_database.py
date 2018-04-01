import pytest

import app as rb_backend

def test_database(app):
   with app.app_context():
      db_client = rb_backend.database.get_db_client()
      assert db_client.db.command('ping')

   app.config['MONGO_HOST'] =  'this defenitly not a good parameter'
   with app.app_context(), pytest.raises(rb_backend.errors.DatabaseError):
      db_client = rb_backend.database.get_db_client()
