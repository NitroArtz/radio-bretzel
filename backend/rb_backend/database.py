import abc

from flask import current_app as app
from flask_pymongo import PyMongo

from rb_backend.errors import DatabaseError

_models = [
   'channels',
]

def get_database():
   if not hasattr(app, 'db'):
      try:
         mongo = PyMongo(app)
         app.db = mongo.db
         app.db.command('ping')
      except Exception as e:
         raise DatabaseError("Couldn't initiate database connection : " + str(e))
   return app.db

class Model(dict):
   """ Abstract class whose different models will inherit """
   __metaclass__ = abc.ABCMeta
   
   @staticmethod
   def get_collection(model):
      """ Returns collection object from given model class"""
      db = get_database()
      name = model.__name__.lower()
      if name in _models:
         collection = db[name]
         return collection
      else:
         raise DatabaseError("Couldn't get collection : Unreferenced model ''" + name + "'")

   @classmethod
   @abc.abstractmethod
   def get(cls, **filters):
      """ Returns multiple matching documents from given filters """
      raise NotImplementedError('Need to implement Model.get_all()')

   @classmethod
   @abc.abstractmethod
   def get_one(cls, _id, **filters):
      """ Returns the first matching document from given filters """
      raise NotImplementedError('Need to implement Model.get_one()')

   @classmethod
   @abc.abstractmethod
   def save(cls, instance):
      """ Create or update document in database """
      raise NotImplementedError('Need to implement Model.save()')

   @classmethod
   @abc.abstractmethod
   def delete(cls, instance):
      """ Delete the current document from given collection """
