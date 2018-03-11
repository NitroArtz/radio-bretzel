import pytest

from flask import Flask
import app as code

@pytest.fixture
def app():
   return code.create_app('test')

@pytest.fixture
def app_no_docker():
   instance = Flask(__name__)
   code.load_config(instance, 'test')
   instance.config['DOCKER_URL'] = ''
   return instance

@pytest.fixture
def app_no_db():
   instance = Flask(__name__)
   code.load_config(instance, 'test')
   instance.config['MONGO_HOST'] = ''
   return instance



def test_connection_no_docker(app_no_docker):
   with pytest.raises(Exception):
      app_not_initialized.docker.init_docker(app_no_docker)

def test_connection_no_db(app_no_db):
   with pytest.raises(Exception):
      code.database.connect_db(app_no_db)



def test_connections(app):
   assert hasattr(app, 'docker') == True
   assert app.docker.ping() == True
   assert hasattr(app, 'mongo') == True

def test_slash(app):
   with app.test_client() as client:
      response = client.get('/')
      assert response.status_code == 200
      assert b'Welcome to Radio Bretzel' == response.get_data()
