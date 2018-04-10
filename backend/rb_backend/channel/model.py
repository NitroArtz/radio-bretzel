import abc

from rb_backend.channel.source.dockerSource import DockerSource
from rb_backend.config import get_config
from rb_backend.database import Model
from rb_backend.errors import DatabaseError, SourceError, ValidationError
from rb_backend.utils import formats, validations

class Channels(Model):
   """ Channel's model definition """
   __metaclass__ = abc.ABCMeta

   @staticmethod
   def validate(check_mandatories=True, **data):
      """ Validate Channel arguments """
      valids = {}
      invalids = {}
      mandatories = ['slug']
      if check_mandatories: validations.check_mandatories(data, *mandatories)
      for key,value in data.items():
         try:
            if key == 'uuid': valids[key] = validations.uuid(value)
            elif key == 'slug': valids[key] = validations.slug(value)
            elif key == 'active': valids[key] = validations.bool(value)
            elif key == 'name': valids[key] = validations.text(value, max_length=32)
            elif key == 'description': valids[key] = validations.text(value)
            elif key == 'source_name': valids[key] = validations.slug(value)
            elif key == 'source_stream_mountpoint': valids[key] = validations.slug(value)
            else: raise ValidationError('Unreferenced argument')
         except ValidationError as e:
            invalids[key] = str(e)
      valids.pop('source_args', False)
      if invalids:
         raise ValidationError(invalids)
      return valids

   @classmethod
   @abc.abstractmethod
   def find(cls, **filters):
      """ Returns all matching channels from given filters
      """
      collection = Model.get_collection(cls)
      soft_deleted = validations.bool(filters.pop('soft_deleted', 'false'))
      filters = Channels.validate(check_mandatories=False, **filters)
      if not soft_deleted: filters.update({'soft_deleted': soft_deleted})
      items = []
      for document in collection.find(filters):
         slug = document.pop('slug')
         channel = Channel(slug, **document)
         items.append(channel)
      return items

   @classmethod
   @abc.abstractmethod
   def find_one(cls, slug, **filters):
      """ Returns the first matching channel from given filters
      """
      collection = Model.get_collection(cls)
      soft_deleted = validations.bool(filters.pop('soft_deleted', 'false'))
      filters = Channels.validate(filters.update({'slug': slug}))
      if not soft_deleted: filters.update({'soft_deleted': soft_deleted})
      document = collection.find_one(filters)
      if not document:
         raise DatabaseError('No channel named ' + str(slug) + 'found')
      slug = document.pop('slug')
      return Channel(slug, **document)

   @classmethod
   @abc.abstractmethod
   def create(cls, slug, **kwargs):
      """ Returns the created channel from given arguments
      """
      collection = Model.get_collection(cls)
      force_source_creation = validations.bool(kwargs.pop('force_source_creation', 'False'))
      kwargs = Channels.validate(kwargs.update({'slug': slug}))
      document = collection.find_one(kwargs)
      if document:
         raise DatabaseError("channel with slug " + str(slug) + " already exists")
      kwargs.update({'force_source_creation': force_source_creation})
      channel = Channel(slug, **kwargs)
      collection.insert_one(channel._document())
      return channel

   @classmethod
   @abc.abstractmethod
   def update(cls, slug, values):
      """ Returns the first matching channel with given slug , updated with
      given arguments
      """
      collection = Model.get_collection(cls)
      slug = validations.slug(slug)
      values.pop('slug', False)
      values = Channels.validate(values, check_mandatories=False)
      channel = Channels.find_one(slug)
      vars(channel).update(values)
      collection.replace_one({'slug': slug}, channel._document())
      return channel

   @classmethod
   @abc.abstractmethod
   def delete(cls, slug, soft=False):
      collection = Model.get_collection(cls)
      slug = validations.slug(slug)
      channel = Channels.find_one(slug, **{'soft_deleted': 'true'})
      try: channel.source.delete(force=True)
      except: pass
      if soft:
         channel.soft_deleted = True
         collection.replace_one({'slug': slug}, channel._document())
      else:
         collection.delete_one({'slug': channel.slug})
      return channel


class Channel(object):

   _source_class = None
   source = None
   source_args = {}

   def __init__(self,
               slug,
               **kwargs):
      """ Channel object constructor.

      Arguments :
      slug      (Mandatory)   <string> :  Channel's global id, uniquely composed of
                                          alphanumeric characters and up to 2 dashes
      active                  <bool>   :  Administrative enabled / disabled value
      soft_deleted            <bool>   :  Administrative soft_deleted value
      name                    <string> :  Channel's public name
      description             <string> :  Channel's description
      source_args             <dict>   :  dictionnary containing source arguments.
                                          will be overriden by source_ prefixed args
                                          This overrides the given source_args attribute
      force_source_creation   <bool>   :  If set to True (False by default), potential
                                          existing source will be overriden at channel
                                          creation
      """
      config = get_config()
      self.slug = slug
      self.active = kwargs.pop('active', True)
      self.soft_deleted = kwargs.pop('soft_deleted', False)
      self.name = kwargs.pop('name', formats.id_to_name(slug))
      self.description = kwargs.pop('description', "Welcome to " + self.name + ", my super Radio Bretzel Channel")
      self.source_args = kwargs.pop('source_args', {})
      self.source_args['name'] = self.source_args.get('name', config['OBJECTS_NAME_PREFIX'] + 'source_' + self.slug)
      if self.active and not self.soft_deleted:
         self.init_source(force_creation=kwargs.pop('force_source_creation', False))

   def _document(self):
      """ Channel model database schema """
      document = vars(self).copy()
      document.pop('source', False)
      document.pop('_source_class', False)
      return document

   def init_source(self, force_creation=False, silent=False):
      config = get_config()
      if config['SOURCE_TYPE'] == 'docker': self._source_class = DockerSource
      source_args = self.source_args.copy()
      source_name = source_args.pop('name')
      try:
         self.source = self._source_class(source_name, force_creation=force_creation, **source_args)
         return self.source
      except Exception as e:
         if silent: return False
         raise SourceError("Couldn't init channel's source : " + str(e))
