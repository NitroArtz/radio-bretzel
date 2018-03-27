from flask import current_app as app

from app import utils
from app.docker import get_docker_client, get_docker_network
from app.errors import DockerError

from app.channel.source import Source

class DockerSource(Source):
   """ DockerSource objects represent liquidsoap containers """

   def __init__(self,
               name,
               streaming_mountpoint):
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
      self.__args = app.config.get_namespace('SOURCE_CONTAINER_')
      self.__image = self.__args.pop('image')
      self.__args.update(default_config)



   def create(self):
      """ Create a source container from given args
      """
      docker_client = get_docker_client()
      try:
         docker_client.containers.get(self.name)
         # If no error is raised before this point, that means
         # we found a matching container.
         raise DockerError()
      except DockerError:
         raise DockerError("Couldn't create source container : already exists")
      except:
         pass

      try:
         container = docker_client.containers.create(image=self.__image, **self.__args)
      except:
         self.remove()
         raise DockerError("Couldn't create source container")

      if app.config['SOURCE_NETWORK'] == True:
         network_config = app.config.get_namespace('SOURCE_NETWORK_')
         network_name = network_config.pop('name')
         source_network = get_docker_network(network_name, **network_config)
         try:
            source_network.connect(container)
         except Exception as e:
            self.remove()
            raise DockerError("Couldn't connect source to sources network")
      return container

   def __get(self):
      """ Return source container object and return False if
      doesn't exists
      """
      docker_client = get_docker_client()
      try:
         container = docker_client.containers.get(self.name)
         return container
      except:
         raise DockerError("Couldn't get source container : no container found")

   def start(self):
      container = self.__get()
      if container:
         try:
            container.start()
            return True
         except:
            pass
      raise DockerError("Couldn't start source container")

   def stop(self):
      container = self.__get()
      if container:
         try:
            container.stop()
            return True
         except:
            pass
      raise DockerError("Couldn't stop source container")

   def status(self):
      container = self.__get()
      try:
         if container:
            return container.status
      except:
         raise DockerError("Couldn't get container status")

   def remove(self, force=False):
      if self.status() == 'running':
         if force:
            self.stop()
         else:
            raise DockerError("Couldn't remove a running source - use force arg to force deletion")
      try:
         container = self.__get()
         if container:
            return container.remove()
      except:
         raise DockerError("Couldn't remove source container")
