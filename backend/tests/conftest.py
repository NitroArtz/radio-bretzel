import pytest

import app as rb_backend


@pytest.fixture
def app():
   return rb_backend.create_app('test')

@pytest.fixture
def client(app):
   return app.test_client()
