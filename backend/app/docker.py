import docker

def connect_docker(config):
   """ Create a connection to docker server, and return the client object """
   client = docker.DockerClient(
      base_url=config["url"],
      version=config["version"]
   )
   return client

def init_docker(app):
   """ Function launched at application startup """
   if not hasattr(app, 'docker'):
      app.docker = connect_docker(app.config.get_namespace('DOCKER_'))
   app.source_network = get_or_create_source_network(app)
   return app

def get_source_network_name(app):
   """ Get source network name from config """
   return app.config['OBJECTS_NAME_PREFIX'] + app.config['SOURCE_NETWORK']

def get_source_network(app):
   """ Returns a docker network object if found, false if not """
   if hasattr(app, 'source_network'):
      return app.source_network
   try:
      network = app.docker.networks.list(get_source_network_name(app))
   except:
      return False

def create_source_network(app):
   """ Create docker network for sources """
   network_config = app.config.get_namespace('SOURCE_NETWORK_')
   network_name = get_source_network_name(app)
   if not hasattr(app, 'source_network'):
      app.source_network = app.docker.networks.create(network_name, **network_config)
   return app.source_network

def get_or_create_source_network(app):
   network = get_source_network(app)
   if not network:
      network = create_source_network(app)
   if not network:
      return False
   else:
      return network
