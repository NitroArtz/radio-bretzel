import docker

from flask import current_app as app

def init_docker(app):
   """ Function launched at application startup.
       Create a connection to docker server.       """
   if not hasattr(app, 'docker'):
      config = app.config.get_namespace('DOCKER_')
      app.docker = docker.DockerClient(
         base_url=config["url"],
         version=config["version"]
      )
   return app

def get_source_network_name():
   """ Get source network name from config """
   return app.config['OBJECTS_NAME_PREFIX'] + app.config['SOURCE_NETWORK']

def create_source_network():
   """ Create docker network for sources """
   network_config = app.config.get_namespace('SOURCE_NETWORK_')
   network_name = get_source_network_name()

   source_network = app.docker.networks.create(network_name, **network_config)
   if not source_network:
      return False
   app.source_network = source_network
   return app.source_network

def get_source_network():
   """ Returns a docker network object if found, create it if not """
   if hasattr(app, 'source_network'):
      return app.source_network
   networks = app.docker.networks.list(get_source_network_name())
   if not networks:
      network = create_source_network()
      if not network:
         raise SystemError("Couldn't create source network")
         return False
   elif len(networks) > 1:
      raise SystemError('matched multiple Docker "' + get_source_network_name() + '" networks')
      return False
   else:
      network = networks[0]
      app.source_network = network
      return network
