from flask import current_app as app

from rb_backend import utils
from rb_backend.docker import get_docker_client, get_docker_network
from rb_backend.errors import DockerError

from rb_backend.channel.source import Source

class DockerSource(Source):
   """ DockerSource objects represent liquidsoap containers """

   def __init__(self,
               name,
               streaming_mountpoint,
               force_creation=False):
      self.name = app.config['OBJECTS_NAME_PREFIX'] + 'source_' + name
      stream_config = app.config.get_namespace('STREAM_')
      default_config = {
         'name': self.name,
         'detach': True,
         'read_only': True,
         'environment': {
            'STREAM_HOST': stream_config['host'],
            'STREAM_SOURCE_PASSWD': stream_config['source_passwd'],
            'STREAM_MOUNTPOINT': streaming_mountpoint
         }
      }
      self._args = app.config.get_namespace('SOURCE_CONTAINER_')
      self._image = self._args.pop('image')
      self._args.update(default_config)
      if force_creation or not self._get(silent=True):
         self.create(force_creation)



   def create(self, override=False):
      """ Create a source container from given args
      """
      docker_client = get_docker_client()
      if self._get(silent=True):
         if not override:
            raise DockerError("container '" + self.name + "' already exists")
         try:
            self.remove(force=True)
         except:
            raise DockerError("Couldn't create source container : " + str(e))
      try:
         container = docker_client.containers.create(image=self._image, **self._args)
      except Exception as e:
         raise DockerError("Couldn't create source container : " + str(e))

      if app.config['SOURCE_NETWORK']:
         network_config = app.config.get_namespace('SOURCE_NETWORK_')
         network_name = network_config.pop('name')
         source_network = get_docker_network(network_name, **network_config)
         try:
            source_network.connect(container)
         except Exception as e:
            self.remove()
            raise DockerError("Couldn't connect source to sources network : " + stre(e))
      return True

   def _get(self, silent=False):
      """ Return source container object and return False if
      doesn't exists
      """
      docker_client = get_docker_client()
      try:
         container = docker_client.containers.get(self.name)
         return container
      except:
         if silent:
            return False
         raise DockerError("source not found")

   def start(self):
      try:
         container = self._get()
         container.start()
         return True
      except Exception as e:
         raise DockerError("Couldn't start source : " + str(e))

   def stop(self):
      try:
         container = self._get()
         container.stop()
         return True
      except Exception as e:
         raise DockerError("Couldn't stop source : " + str(e))

   def status(self):
      try:
         container = self._get()
         return container.status
      except Exception as e:
         raise DockerError("Couldn't get source status : " + str(e))

   def remove(self, force=False):
      try:
         container = self._get()
         if container.status == 'running':
            if not force:
               raise DockerError("couldn't remove a running source. Use force arg to force deletion")
            container.stop()
         container.remove()
         return True
      except Exception as e:
         raise DockerError("Couldn't remove source : " + str(e))
