from flask import current_app as app

from app.docker import get_source_network
from app.errors import DockerError

class DockerSource(object):
   """ DockerSource objects represent liquidsoap containers """
   def __init__(self, channel_name):
      stream_config = app.config.get_namespace('STREAM_')
      self.name = app.config['OBJECTS_NAME_PREFIX'] + 'source_' + channel_name
      self.args = {
         'name': self.name,
         'detach': True,
         'read_only': True,
         'environment': {
            'STREAM_MOUNTPOINT': channel_name,
            'STREAM_HOST': stream_config['host'],
            'STREAM_SOURCE_PASSWD': stream_config['source_passwd']
         },
      }

   def create(self):
      """ Create a source container from given args """
      source_container_config = app.config.get_namespace('SOURCE_CONTAINER_')
      source_container_config.update(self.args)
      try:
         source = app.docker.containers.create(image=app.config['SOURCE_IMAGE'], **source_container_config)
      except:
         raise DockerError("Couldn't create source container")
      try:
         source_network = get_source_network()
         source_network.connect(source)
         return source
      except:
         raise DockerError('Couldn\'t connect source to sources network')

   def get(self):
      """ Return source container object or create it if doesn't exist. """
      try:
         source = app.docker.containers.get(self.name)
         return source
      except:
         try:
            source = self.create()
            return source
         except Exception as e:
            raise e

   def start(self):
      try:
         container = self.get()
         container.start()
         return True
      except:
         raise DockerError("Couldn't start source container")

   def stop(self):
      try:
         container = self.get()
         container.stop()
         return True
      except:
         raise DockerError("Couldn't stop source container")

   def status(self):
      try:
         container = self.get()
         return container.status
      except:
         raise DockerError("Couldn't get container status")

   def reload_source(self):
      return True

   def delete_source(self):
      return app.docker.containers.remove(self.name)
