from flask import current_app as app

from flask_pymongo import PyMongo

def connect_db(app):
   """ Open a Mongodb connection."""
   client = PyMongo(app)
   return client

def init_db(app):
   """ Initiate DB connection at app startup """
   if not hasattr(app, 'database'):
      app.mongo = connect_db(app)
   return app

class Document(object):
   """ Abstract class whose different models will inherit """

   def save(collection, document):
      """ Update or create provided document from given collection """
      if not document.get('_id'):
         return False
      try:
         collection.find_one({'_id': document['_id']})
      except:
         collection.insert_one(document)
      else:
         collection.replace_one({'_id': document['_id']}, document)
      return True

   def delete(self):
      """ Delete the current document from given collection """
      if not document.get('_id'):
         return False
      try:
         collection.find_one({'_id': document['_id']})
      except:
         return False
      collection.remove({'_id': document['_id']})
      return True
