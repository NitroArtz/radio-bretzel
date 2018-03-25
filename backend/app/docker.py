import docker, time

from app.config import get_config
from app.errors import DockerError

def get_docker_client(config=None):
   """ Returns an instance of docker client
   """
   config = get_config(config, DockerError("Couldn't initiate docker connection"))
   docker_config = config.get_namespace('DOCKER_')
   url = docker_config.pop('url')
   version = docker_config.pop('version')
   try:
      client = docker.DockerClient(
         base_url=url,
         version=version,
         **docker_config)
      return client
   except Exception as e:
      raise DockerError("Couldn't init docker connection : couldn't connect to server")


def get_docker_network(name, **config):
   """This function returns a docker network depending on configuration given.
   Create the network if not found.
   """
   docker_client = get_docker_client()
   networks = docker_client.networks.list(name)
   if not networks:
      return docker_client.networks.create(name, **config)
   elif len(networks) > 1:
      raise DockerError('Matched multiple Docker networks named '+ name)
   else:
      network = networks[0]
   if not network:
      raise DockerError("Couldn't find nor create docker source network")
   return network
