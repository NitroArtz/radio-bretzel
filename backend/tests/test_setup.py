import pytest

from flask import Flask
import app as radiobretzel

@pytest.fixture
def app():
   return radiobretzel.create_app('test')

@pytest.fixture
def app_no_docker():
   instance = Flask(__name__)
   radiobretzel.load_config(instance, 'test')
   instance.config['DOCKER_URL'] = ''
   return instance

@pytest.fixture
def app_no_db():
   instance = Flask(__name__)
   radiobretzel.load_config(instance, 'test')
   instance.config['MONGO_HOST'] = ''
   return instance

def test_connection_no_docker(app_no_docker):
   with pytest.raises(Exception):
      app_not_initialized.docker.init_docker(app_not_initialized)

def test_connection_no_db(app_no_db):
   with pytest.raises(Exception):
      radiobretzel.database.connect_db(app_not_initialized)



def test_connections(app):
   assert hasattr(app, 'docker') == True
   assert app.docker.ping() == True
   assert hasattr(app, 'mongo') == True
   assert app.mongo.server_info() != None

#def test_slash(app):
