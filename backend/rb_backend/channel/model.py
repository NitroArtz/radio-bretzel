from flask import current_app as app

from rb_backend.database import Document
from rb_backend.utils import formats, validations

from rb_backend.channel.source.dockerSource import DockerSource


class Channel(Document):
   model = 'channel'

   def get_all():
      return Document.get_all(Channel.model)

   def get_one(_id, **filters):
      document = Document.get_one(Channel.model, _id, **filters)


   def __init__(self,
               _id,
               name=None,
               streaming_mountpoint=None,
               source_name=None,
               force_source_creation=False):
      self._id = _id
      self.name = formats.id_to_name(_id, name)
      self.streaming_mountpoint = streaming_mountpoint or _id
      self.source_name = source_name or _id
      self.init_source(force_creation=force_source_creation)

   def init_source(self, force_creation=False):
      if app.config['SOURCE_TYPE'] == 'docker':
         self.__source_class = DockerSource
      self.source = self.__source_class(self.source_name, self.streaming_mountpoint, force_creation=force_creation)

   def document(self):
      return {
         '_id': self._id,
         'name': self.name,
         'source': {
            'name': self.source.name,
         }
      }

   def info(self):
      info = self.document()
      info['source']['status'] = self.source.status()
      return info

def validate(**data):
   """ Validate Channel arguments """
   valid = {}
   invalids = {}
   for field in data:
      if field == '_id':
         try:
            if not data['_id']:
               raise ValueError('Mandatory argument "_id" not found.')
            validations.slug(data['_id'])
            valids[field] = data[field]
         except ValueError as e:
            invalids['_id'] = e.message

   return valids, invalids
