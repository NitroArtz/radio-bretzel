from flask import current_app as app

from app.database import Document
from app.utils import formats, validations

from app.channel.source.dockerSource import DockerSource


class Channel(Document):
   model = 'channel'

   def __init__(self,
               _id,
               name=None):
      self._id = _id
      self.name = formats.id_to_name(_id, name)
      streaming_mountpoint = _id
      if app.config['SOURCE_TYPE'] == 'docker':
         self.source = DockerSource(_id, streaming_mountpoint)

   def get_all():
      return Document.get_all('channel')

   def info(self):
      info = vars(self)
      info['source'] = {
         'name': self.source.name,
         'status': self.source.status()
      }
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
