import os
from flask import Flask

from app import config, docker
from app.database import init_db
from app.docker import init_docker
from app.channel import channel

def create_app(env=None):
   """ Main application entry point """
   if not env:
      env = os.environ.get('RADIO_BRETZEL_ENV', 'development')

   app = Flask(__name__)

   load_config(app, env)
   register_modules(app)
   register_blueprints(app)
   register_main_routes(app)
   # register_teardown(app)

   return app

def load_config(app, env):
   """ Load app configuration """
   if env == 'development':
      app.config.from_object(config.development)
   elif env == 'test':
      app.config.from_object(config.test)
   else:
      raise ValueError('environment variable not supported ('+ env + ')')
   try:
      app.config.from_pyfile('local.py')
   except:
      pass

def register_modules(app):
   """ Activate Flask extensions and initiate external connections """
   init_db(app)
   init_docker(app)

def register_blueprints(app):
   """ Register blueprints with the Flask application. """
   app.register_blueprint(channel, url_prefix='/channel')

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
