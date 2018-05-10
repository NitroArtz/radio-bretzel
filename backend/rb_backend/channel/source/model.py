import abc

from rb_backend.config import get_config
from rb_backend.database import Model
from rb_backend.errors import SourceError, ValidationError, DatabaseError, DatabaseNotFound
from rb_backend.channel.source.dockerSource import DockerSource
from rb_backend.utils import formats
from rb_backend.utils.validations import validate

class Sources(Model):
   """ Sources.init's model definition """
   __metaclass__ = abc.ABCMeta

   @staticmethod
   def init(name, **kwargs):
      config = get_config()
      source_type = config.get('SOURCE_TYPE', 'docker')
      if source_type == 'docker':
         source_class = DockerSource
      else :
         raise ValueError('unsupported source type ' + str(source_type))
      source = source_class(name, **kwargs)
      source.channel = kwargs.get('channel')
      source.setup(kwargs.get('status', 'non-existent'))
      return source


   @staticmethod
   def _schema():
      return {
         'name': {
            'required': True,
            'validator': 'slug'
         },
         'channel': {
            'required': True,
            'validator': 'slug'
         },
         'status': {
            'allowed': ['playing', 'stopped', 'non-existent', 'in error']
         },
         'stream_host': {
            'validator': 'url'
         },
         'stream_port': {
            'type': 'integer',
            'coerce': int
         },
         'stream_mountpoint': {
            'validator': 'slug'
         }
      }

   @classmethod
   @abc.abstractmethod
   def find(cls, **filters):
      """ Returns multiple matching documents from given filters
      """
      collection = Model.get_collection(cls)
      schema = Sources._schema()
      filters = validate(filters, schema, mandatories=False)
      source_list = []
      for document in collection.find(filters):
         name = document.pop('name')
         source = Sources.init(name, **document)
         source_list.append(source)
      return source_list


   @classmethod
   @abc.abstractmethod
   def find_one(cls, **filters):
      """ Returns the first matching document from given filters
      """
      collection = Model.get_collection(cls)
      schema = Sources._schema()
      filters = validate(filters, schema, mandatories=False)
      if not filters: raise ValidationError('You must provide at least one filter')
      try:
         document = collection.find_one(filters)
      except Exception as e:
         raise DatabaseError(str(e))
      if not document: raise DatabaseNotFound()
      name = document.pop('name')
      return Sources.init(name, **document)


   @classmethod
   @abc.abstractmethod
   def create(cls, **kwargs):
      """ Returns new document from given args
      """
      collection = Model.get_collection(cls)
      schema = Sources._schema()
      values = validate(kwargs, schema)
      name = values.pop('name')
      values['status'] = values.get('status', 'stopped')
      for document in collection.find({'name': name}).limit(1):
         if document: raise ValueError("source '" + str(name) + "' already exists.")
      source = Sources.init(name, **values)
      try:
         collection.insert_one(source._document())
      except Exception as e:
         DatabaseError(str(e))
      return source

   @classmethod
   @abc.abstractmethod
   def update(cls, source, **values):
      """ Update given source with given values. Sources.init can be source object or source name
      """
      collection = Model.get_collection(cls)
      if isinstance(source, str):
         source = Sources.find_one(**{'name': source})
      schema = Sources._schema()
      formats.pop_keys(schema, 'name', 'channel', 'status')
      values = validate(values, schema, mandatories=False)
      vars(source).update(values)
      try:
         source.reload()
      except:
         pass
      try:
         collection.update_one(
            {'name': source.name},
            {'$set': source._document()}
         )
         return source
      except Exception as e:
         raise DatabaseError(str(e))

   @classmethod
   @abc.abstractmethod
   def delete(cls, source, force='false'):
      """ Delete the current document from given collection
      """
      collection = Model.get_collection(cls)
      if isinstance(source, str):
         source = Sources.find_one(**{'name': source})
      schema = {
         'force': {
            'validator': 'boolean',
            'coerce': 'boolean'
         }
      }
      force = validate({'force': force}, schema).pop('force')
      source.delete(force=force)
      try:
         collection.delete_one({'name': source.name})
         return source
      except:
         raise DatabaseError(str(e))
