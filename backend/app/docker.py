import docker

from .errors import DockerError

def init_docker(app):
   """ Function launched at application startup.
       Create a connection to docker server.       """
   config = app.config.get_namespace('DOCKER_')
   try:
      app.docker = docker.DockerClient(
         base_url=config["url"],
         version=config["version"]
      )
      return app
   except Exception as e:
      raise DockerError("Couldn't init docker connection : " + e.message)

def get_source_network_name(app):
   """ Get source network name from config """
   return app.config['OBJECTS_NAME_PREFIX'] + app.config['SOURCE_NETWORK']

def create_source_network(app):
   """ Create docker network for sources """
   network_config = app.config.get_namespace('SOURCE_NETWORK_')
   network_name = get_source_network_name(app)
   try:
      source_network = app.docker.networks.create(network_name, **network_config)
      if not source_network:
         raise DockerError("Couldn't create source network")
      app.source_network = source_network
      return app.source_network
   except Exception as e:
      raise e

def get_source_network(app):
   """ Returns a docker network object if found, create it if not """
   if hasattr(app, 'source_network'):
      return app.source_network
   try:
      networks = app.docker.networks.list(get_source_network_name(app))
      if not networks:
         network = create_source_network(app)
      elif len(networks) > 1:
         raise DockerError('matched multiple Docker "' + get_source_network_name(app) + '" networks')
      else:
         network = networks[0]
      if not network:
         raise DockerError("Couldn't create source network")
      app.source_network = network
      return network
   except Exception as e:
      raise e
