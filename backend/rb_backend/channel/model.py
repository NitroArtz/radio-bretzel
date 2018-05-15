import abc

from rb_backend.config import get_config
from rb_backend.database import Model
from rb_backend.errors import DatabaseError, DatabaseNotFound, SourceError, ValidationError
from rb_backend.source.model import Sources
from rb_backend.source import source as Source
from rb_backend.utils import formats
from rb_backend.utils.validations import validate

class Channels(Model):
   """ Channel's model definition """
   __metaclass__ = abc.ABCMeta

   _schema = {
         'slug': {
            'required': True,
            'validator': 'slug',
         },
         'name': {
            'validator': 'text'
         },
         'active': {
            'validator': 'boolean',
            'coerce': 'boolean',
            'default': True
         },
         'deleted': {
            'validator': 'boolean',
            'coerce': 'boolean',
            'default': False
         },
         'description': {
            'validator': 'text'
         },
         'source': {
            'oneof': [
               {
                  'validator': 'slug',
                  'nullable': True
               },
               {
                  'type': 'dict',
                  'valueschema': Sources._schema
               }
            ]
         }
      }

   @classmethod
   @abc.abstractmethod
   def find(cls, **filters):
      """ Returns all matching channels from given filters
      """
      collection = Model.get_collection(cls)
      schema = Channels._schema.copy()
      filters = validate(filters, schema, mandatories=False)
      show_deleted = filters.pop('deleted', False)
      if not show_deleted:
         filters['deleted'] = False
      channel_list = []
      pipeline = [
         {
            '$match': filters
         },
         {
            '$lookup': {
               'from': 'sources',
               'localField': 'source',
               'foreignField': 'channel',
               'as': 'source'
            }
         },
         {
            '$unwind': {
               'path': '$source'
            }
         }
      ]
      try:
         for document in collection.aggregate(pipeline):
            channel = Channel(**document)
            channel_list.append(channel)
      except SourceError:
         raise
      except Exception as e:
         raise DatabaseError(str(e))
      return channel_list

   @classmethod
   @abc.abstractmethod
   def find_one(cls, **kwargs):
      """ Returns the first matching channel from given name
      """
      collection = Model.get_collection(cls)
      schema = Channels._schema.copy()
      channel = Channels.find_one(**{'slug': channel})
      filters = validate(filters, schema, mandatories=False)
      show_deleted = filters.pop('deleted', False)
      if not show_deleted:
         filters['deleted'] = False
      pipeline = [
         {
            '$match': filters
         },
         {
            '$limit': 1
         },
         {
            '$lookup': {
               'from': 'sources',
               'localField': 'source',
               'foreignField': 'channel',
               'as': 'source'
            }
         },
         {
            '$unwind': {
               'path': '$source'
            }
         },

      ]
      document_list = []
      try:
         for document in collection.aggregate(pipeline):
            channel_list.append(document)
      except SourceError:
         raise
      except Exception as e:
         raise DatabaseError(str(e))
      document = documents.pop()
      return Channel(**document)

   @classmethod
   @abc.abstractmethod
   def create(cls, **kwargs):
      """ Returns the created channel from given arguments
      """
      collection = Model.get_collection(cls)
      schema = Channels._schema.copy()
      values = validate(kwargs, schema)
      slug = values.get('slug')
      for document in collection.find({'slug': slug}).limit(1):
         if document: raise ValueError("channel " + str(e) + " already exists.")
      source_args = values.pop('source', {})
      if not source_args.get('name'):
         source_args['name'] = slug
      source_args['channel'] = slug
      if not source_args.get('status'):
         values['source'] = Sources.create(**source_args)
      channel = Channel(**values)
      try:
         collection.insert_one(channel._document)
      except Exception as e:
         DatabaseError(str(e))
      return channel

   @classmethod
   @abc.abstractmethod
   def update(cls, channel, values):
      """ Returns the first matching channel with given slug , updated with
      given arguments
      """
      collection = Model.get_collection(cls)
      if isinstance(channel, str):
         channel = Channels.find_one(**{'slug': channel})
      schema = Channels._schema.copy()
      formats.pop_keys(schema, 'source')
      values = validate(values, schema, mandatories=False)
      vars(channel).update(values)
      if values:
         try:
            source.reload()
         except:
            pass
      try:
         collection.update_one(
            {'slug': channel.slug},
            {'$set': channel._document}
         )
      except Exception as e:
         raise DatabaseError(str(e))
      return channel

   @classmethod
   @abc.abstractmethod
   def delete(cls, channel, hard_delete='false'):
      collection = Model.get_collection(cls)
      schema = {
         'hard_delete': {
            'validator': 'boolean',
            'coerce': 'boolean'
         }
      }
      hard_delete = validate(values, schema).pop('hard_delete')
      if isinstance(channel, str):
         channel = Channels.find_one(**{'slug': channel})
      if not hard_delete:
         channel.source.delete(force=True)
         try:
            collection.update_one(
               {'slug': channel.slug},
               {'$set': {'deleted': True, 'source': None}}
            )
         except Exception as e:
            raise DatabaseError(str(e))
      else:
         Sources.delete(channel.source, force=True)
         try:
            collection.delete_one({'slug': channel.slug})
         except Exception as e:
            raise DatabaseError(str(e))
      return channel


class Channel(object):
   """ Channel object.
   """
   def __init__(self, **kwargs):
      config = get_config()
      self.slug = kwargs.pop('slug')
      self.active = kwargs.pop('active', True)
      self.soft_deleted = kwargs.pop('soft_deleted', False)
      self.name = kwargs.pop('name', formats.id_to_name(self.slug))
      self.description = kwargs.pop('description', "Welcome to " + self.name + " Radio Bretzel Channel")
      source = kwargs.pop('source', None)
      if isinstance(source, dict):
         self.source = Source.init(**source)
      else:
         self.source = source

   @property
   def _document(self):
      """ Channel model database schema """
      document = vars(self).copy()
      document.pop('source', False)
      try:
         document['source'] = self.source.name
      except:
         document['source'] = None
      return document
