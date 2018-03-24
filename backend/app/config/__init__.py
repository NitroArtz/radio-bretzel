import os

from flask import Config as FlaskConfig
from flask import current_app as app

class Config(FlaskConfig):
   """Main configuration class. This class will be used normally by Flask and  as a singleton by our app, in order to prevent any unexpected behaviour
   """

   def load(self, env=None, local_config_file=None):
      """ Load app configuration """

      if not env:
         env = os.environ.get('RADIO_BRETZEL_ENV', 'development')
      if not local_config_file:
         local_config_file = os.environ.get('RADIO_BRETZEL_CONFIG_FILE', 'local.py')
      config_file = 'config/'

      self.from_pyfile('config/default.py')

      if env == 'development':
         self.from_pyfile('config/development.py')
      elif env == 'test':
         self.from_pyfile('config/test.py')
      else:
         raise ValueError('environment variable not supported ('+ env + ')')

      try:
         self.from_pyfile('config/' + local_config_file)
      except:
         raise ValueError("Couldn't load config file " + local_config_file)


   def docker_config(self):
      return self.get_namespace('DOCKER_')
