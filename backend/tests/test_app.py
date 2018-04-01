import pytest

import rb_backend

def test_app(app):
   assert app.config['TESTING'] == True


def test_routes(client):
   res = client.get('/')
   assert b'Welcome to Radio Bretzel' in res.data
