import abc

from rb_backend.channel.source.dockerSource import DockerSource
from rb_backend.config import get_config
from rb_backend.database import Model
from rb_backend.errors import DatabaseError, SourceError
from rb_backend.utils import formats, validations

class Channels(Model):
   """ Channel's model definition """
   __metaclass__ = abc.ABCMeta

   @classmethod
   @abc.abstractmethod
   def get(cls, **filters):
      collection = Model.get_collection(cls)
      items = []
      for channel_document in collection.find(**filters):
         _id = channel_document.pop('_id')
         channel = Channel(_id, **channel_document)
         items.append(channel)
      return items

   @classmethod
   @abc.abstractmethod
   def get_one(cls, _id, **filters):
      collection = Model.get_collection(cls)
      channel_document = collection.find_one(_id, **filters)
      if not channel_document:
         raise DatabaseError('Not found')
      _id = channel_document.pop('_id')
      return Channel(_id, **channel_document)

   @classmethod
   @abc.abstractmethod
   def save(cls, channel):
      collection = Model.get_collection(cls)
      try:
         existing_document = collection.find_one(channel._id)
         if existing_document:
            collection.replace_one(existing_document, channel._document())
         else:
            collection.insert_one(channel._document())
         return True
      except Exception as e:
         raise DatabaseError("Couldn't save channel " + channel.name + " in database :" + str(e))

   @classmethod
   @abc.abstractmethod
   def delete(cls, channel, soft=False):
      collection = Model.get_collection(cls)
      channel.source.delete(force=True)
      try:
         if soft:
            channel.active = False
            return Channels.save(channel)
         return collection.delete_one({'_id': channel._id})
      except Exception as e:
         raise DatabaseError("Couldn't delete channel " + channel.name + " in database :" + str(e))

class Channel(object):

   _source_class = None
   source = None
   source_args = {}

   def __init__(self,
               _id,
               **kwargs):
      """ Channel object constructor.
      Arguments :
         _id      (Mandatory)    <string> :  Channel's global id, uniquely composed of
                                             alphanumeric characters and up to 2 dashes
         active                  <bool>   :  Administrative enabled / disabled value
         name                    <string> :  Channel's public name
         source_args             <dict>   :  dictionnary containing source arguments.
                                             will be overriden by source_ prefixed args
                                             This overrides the given source_args attribute
         force_source_creation   <bool>   :  If set to True (False by default), potential
                                             existing source will be overriden at channel
                                             creation
      """
      self._id = _id
      self.active = kwargs.pop('active', True)
      self.name = kwargs.pop('name', formats.id_to_name(_id))
      source_args = kwargs.pop('source_args', {})
      # Default values for source_args here
      self.source_args['name'] = source_args.get('name', False) or _id
      self.init_source(force_creation=kwargs.pop('force_source_creation', False))

   def _document(self):
      document = vars(self).copy()
      document.pop('source', False)
      document.pop('_source_class', False)
      return document

   def init_source(self, force_creation=False, silent=False):
      config = get_config()
      if config['SOURCE_TYPE'] == 'docker':
         self._source_class = DockerSource
      source_args = self.source_args.copy()
      source_name = source_args.pop('name')
      try:
         self.source = self._source_class(source_name, force_creation=force_creation, **source_args)
         return self.source
      except Exception as e:
         if silent:
            return False
         raise SourceError("Couldn't init_source : " + str(e))


def validate(**data):
   """ Validate Channel arguments """
   valid = {}
   invalids = {}
   for field in data:
      try:
         if field == '_id': validations.slug(data['_id'])
         if field == 'name': validations.name()
      except ValueError as e:
         invalids['_id'] = e.message
      valids[field] = data[field]

   return valids, invalids
