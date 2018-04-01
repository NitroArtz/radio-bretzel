import os
from flask import Flask

from rb_backend import channel, database, docker
from rb_backend.config import Config

def create_app(env=None, local_config_file=None, **config):
   """ Main application entry point """
   Flask.config_class = Config

   app = Flask(__name__)
   app.config.load(env, local_config_file, **config)

   register_routes(app)
   register_main_routes(app)
   # register_teardown(app)

   return app

def register_routes(app):
   """ Register routes of submodules. """
   channel.routes(app)

def register_main_routes(app):
   """ Register main routes for application. """
   @app.route('/')
   def hello_world():
      return 'Welcome to Radio Bretzel'

# def register_teardown(app):
#    """Register teardowns """
#    @app.teardown_appcontext
#    def remove_source_network(error):
#       teardown_docker(app)
