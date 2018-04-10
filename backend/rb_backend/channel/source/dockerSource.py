from flask import current_app as app

from rb_backend.config import get_config
from rb_backend.docker import get_docker_client, get_docker_network
from rb_backend.errors import SourceError
from rb_backend.utils import formats

from rb_backend.channel.source import Source

class DockerSource(Source):
   """ DockerSource objects represent liquidsoap containers """

   def __init__(self,
               name,
               **args):
      """
      Arguments:
         name     (Mandatory)    <string> :  source name, uniquely composed of
                                             alphanumeric characters and up to 2 dashes
         stream_host             <string> :  URL of streaming server.
         stream_source_passwd    <string> :  streaming authentication password
         stream_mountpoint       <string> :  streaming mountpoint

      """
      config = get_config()
      stream_config = formats.get_prefixed_keys(config, 'STREAM_')
      self.name = name
      self._args = formats.get_prefixed_keys(config, 'SOURCE_CONTAINER_')
      ct_args = {
         'name': self.name,
         'detach': True,
         'read_only': True,
         'environment': {
            'STREAM_HOST': args.get('stream_host', False) or config['STREAM_HOST'],
            'STREAM_SOURCE_PASSWD': args.get('stream_source_passwd', False) or config['STREAM_SOURCE_PASSWD'],
            'STREAM_MOUNTPOINT': args.get('stream_mountpoint', self.name)
         }
      }
      force_creation = args.pop('force_creation', False)
      self._args.update(ct_args)

      if force_creation or not self._get(silent=True):
         self.create(force_creation)

   def create(self, override=False):
      """ Create a source container from given args
      """
      config = get_config()
      docker_client = get_docker_client()
      if self._get(silent=True):
         if not override:
            raise SourceError("source '" + self.name + "' already exists")
         try:
            self.delete(force=True)
         except Exception as e:
            raise SourceError("Couldn't create source : " + str(e))
      try:
         args = self._args.copy()
         image = args.pop('image', None)
         if not image: raise SourceError('no image name given')
         container = docker_client.containers.create(image=image, **args)
      except Exception as e:
         raise SourceError("Couldn't create source : " + str(e))

      if config['SOURCE_NETWORK']:
         network_config = formats.get_prefixed_keys(config, 'SOURCE_NETWORK_')
         network_name = config['OBJECTS_NAME_PREFIX'] + network_config.pop('name')
         source_network = get_docker_network(network_name, **network_config)
         try:
            source_network.connect(container)
         except Exception as e:
            self.delete()
            raise SourceError("Couldn't connect source to sources network : " + stre(e))
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
         raise SourceError("source not found")

   def start(self):
      try:
         container = self._get()
         container.start()
         return True
      except Exception as e:
         raise SourceError("Couldn't start source : " + str(e))

   def stop(self):
      try:
         container = self._get()
         container.stop()
         return True
      except Exception as e:
         raise SourceError("Couldn't stop source : " + str(e))

   def status(self, silent=False):
      try:
         container = self._get()
         return container.status
      except Exception as e:
         if silent: return "unavailable"
         raise SourceError("Couldn't get source status : " + str(e))

   def delete(self, force=False):
      try:
         container = self._get()
         if container.status == 'running':
            if not force:
               raise SourceError("source is running. Use force arg to force deletion")
            container.stop()
         container.remove()
         return True
      except Exception as e:
         raise SourceError("Couldn't delete source : " + str(e))
