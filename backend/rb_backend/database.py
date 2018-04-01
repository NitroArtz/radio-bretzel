from flask import current_app as app
from flask_pymongo import PyMongo

from rb_backend.errors import DatabaseError

models = [
   'channel',
]

def get_db_client():
   if not hasattr(app, 'mongo'):
      try:
         app.mongo = PyMongo(app)
         app.mongo.db.command('ping')
      except Exception as e:
         raise DatabaseError("Couldn't initiate database connection : " + str(e))
   return app.mongo

def get_collection(name):
   """ Returns collection object from given name """
   mongo = get_db_client()
   if name in models:
      collection = mongo.db[name]
      return collection
   else:
      raise DatabaseError("Couldn't get collection : Unreferenced model name")

class Document(object):
   """ Abstract class whose different models will inherit """

   def get_all(model):
      """ Returns all documents from given model name """
      items = []
      collection = get_collection(model)
      for item in collection.find():
         items.append(item)
      return items

   def document(self):
      raise NotImplemented('Need to implement Document.document(). document(self) must return a dict object containing every fields you want to store in mongodb')

   def save(self):
      """ Update or create model's document in database """
      collection = get_collection(self.model)
      document = self.document()
      try:
         existing_document = collection.find_one({'_id': document['_id']})
         if existing_document:
            collection.replace_one(existing_document, document)
         else:
            collection.insert_one(document)
         return True
      except Exception as e:
         raise DatabaseError("Couldn't save " + self.model + " in database :" + str(e))

   def delete(self):
      """ Delete the current document from given collection """
      collection = get_collection(self.model)
      document = self.document()
      try:
         existing_document = collection.find_one({'_id': document['_id']})
         if not existing_document:
            raise DatabaseError("no document with _id " + document['_id'])
         collection.remove(existing_document)
         return True
      except Exception as e:
         raise DatabaseError("Couldn't delete " + self.model + " in database :" + str(e))
