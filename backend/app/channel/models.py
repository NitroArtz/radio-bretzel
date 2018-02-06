import os, re

from flask import current_app as app

from app.database import Document

class Source(object):
   """ Abstract class whose Channels will inherit """
   def get_container_name(self):
      return app.config['OBJECTS_NAME_PREFIX'] + 'source_' + self._id

   def create_source(self):
      """ Create a source container from given args """
      config = app.config.get_namespace('SOURCE_CONTAINER_')
      container_args = {
         'name': self.get_container_name(),
         'detach': True,
         'read_only': True,
         'network': app.config['OBJECTS_NAME_PREFIX'] + app.config['SOURCE_NETWORK'],
         'auto_remove': True
      }
      config.update(container_args)
      source = app.docker.containers.run(image=app.config['SOURCE_IMAGE'], **config)
      if not source:
         return False
      return source

   def get_source(self):
      """ Return source container object or false if doesn't exist """
      try:
         source = app.docker.containers.get(self.get_container_name())
      except:
         return False
      return source

   def get_or_create_source(self):
      """ Return source container object, and create it if doesn't exist """
      source = self.get_source()
      if not source:
         source = self.create_source()
      if not source:
         return False
      else:
         return source

   def reload_source(self):
      return True

   def delete_source(self):
      return app.docker.containers.remove(self.get_container_name())


class Channel(Source):

   def __init__(self,
                  _id,
                  name=None):
      self._id = _id
      if name:
         self.name = name.title()
      else:
         name = _id.replace('-', ' ')
         self.name = name.title()
      self.source = self.get_or_create_source()

   def document(self):
      document = {
         '_id': self._id,
         'name': self.name,
      }
      return document

   def save(self):
      return Document.save(app.mongo.db.channels, self.document())

   def delete(self):
      return Document.delete(app.mongo.db.channels, self.document())
