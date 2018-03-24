import docker, time

from flask import current_app as app
from app.errors import DockerError

__client = None

def get_docker_client(config=None):
   """ Returns an instance of docker client
   """
   global __client
   if __client:
      return __client
   if not config:
      try:
         config = app.config
      except:
         raise DockerError("Couldn't init docker connection : no config given")
   tries = 0
   while tries < 3:
      tries += 1
      try:
         if not config:
            raise DockerError("Need configuration to start Docker")
         docker_config = config.docker_config()
         __client = docker.DockerClient(
            base_url=docker_config["url"],
            version=docker_config["version"]
         )
         return __client
      except Exception as e:
         if tries == 3:
            raise e
            raise DockerError("Couldn't init docker connection")
         time.sleep(0.5)

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
