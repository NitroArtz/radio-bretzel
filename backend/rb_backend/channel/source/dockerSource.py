from flask import current_app as app

from rb_backend.config import get_config
from rb_backend.docker import get_docker_client, get_docker_network
from rb_backend.errors import DockerError
from rb_backend.utils import formats

from rb_backend.channel.source import Source

class DockerSource(Source):
   """ DockerSource objects represent liquidsoap containers """

   def __init__(self,
               name,
               **args):
      config = get_config()
      self.name = config['OBJECTS_NAME_PREFIX'] + 'source_' + name
      stream_config = formats.get_prefixed_keys(config, 'STREAM_')
      mandatory_args = {
         'name': self.name,
         'detach': True,
         'read_only': True,
         'environment': {
            'STREAM_HOST': stream_config['host'],
            'STREAM_SOURCE_PASSWD': stream_config['source_passwd'],
            'STREAM_MOUNTPOINT': name
         }
      }
      force_creation = args.pop('force_creation', False)
      self._args = formats.get_prefixed_keys(config, 'SOURCE_CONTAINER_')
      if args:
         self._args.update(args)
      self._args.update(mandatory_args)
      if force_creation or not self._get(silent=True):
         self.create(force_creation)



   def create(self, override=False):
      """ Create a source container from given args
      """
      config = get_config()
      docker_client = get_docker_client()
      if self._get(silent=True):
         if not override:
            raise DockerError("container '" + self.name + "' already exists")
         try:
            self.remove(force=True)
         except:
            raise DockerError("Couldn't create source container : " + str(e))
      try:
         args = self._args.copy()
         image = args.pop('image', None)
         if not image: raise DockerError('no image name given')
         container = docker_client.containers.create(image=image, **args)
      except Exception as e:
         raise DockerError("Couldn't create source container : " + str(e))

      if config['SOURCE_NETWORK']:
         network_config = formats.get_prefixed_keys(config, 'SOURCE_NETWORK_')
         network_name = config['OBJECTS_NAME_PREFIX'] + network_config.pop('name')
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
