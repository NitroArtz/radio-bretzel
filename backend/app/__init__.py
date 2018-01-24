from flask import Flask
from flask_pymongo import PyMongo

import docker

from app.api.source import SourceModels

def start(config):
   app = Flask(__name__)
   app.config.from_object(config)

   docker_client = docker.DockerClient(
      base_url=config.DOCKER_URL,
      version=config.DOCKER_VERSION
   )

   mongo_client = PyMongo(app)

   @app.route('/')
   def hello_world():
      return 'Welcome to Radio Bretzel'

   @app.route('/new', methods=['GET','POST'])
   def new():

         source = SourceModels.create(docker_client, 'test_source-creation')
         return source.id

   @app.route('/source', methods=['POST'])
   def source():
      if request.method == 'POST':
         source_data = SourceModels.create_valid_source_data(request.args['id'],
            request.args['active'],
            request.args['name'],
            request.args['container'],
            request.args['description'])
         source = SourceModels.create_source(source_date)
         return source.id

   @app.route('/next')
   def next():
      return SourceModels.select_next_track()

   return app
