import pytest

import rb_backend

def test_app(app):
   assert app.config['TESTING'] == True


def test_default_routes(client):
   res = client.get('/')
   assert b'Welcome to Radio Bretzel' in res.data

# def test_Channels_controller(client):
#    assert client.get('/channel/').data == b'[]\n'
#
#    assert client.get('/channel/test-routes').status_code == 404
#    assert client.post('/channel/test_routes').status_code == 400
#    assert client.post('/channel/test-routes').status_code == 200
#    assert client.get('/channel/test-routes').status_code == 200
#
#    assert client.get('/channel/test-routes/source').status_code == 200
#    assert client.delete('/channel/test-routes/source').status_code == 200
#    assert client.post('/channel/test-routes/source').status_code == 200
#    assert client.post('/channel/test-routes/source/reset').status_code == 200
#    assert client.post('/channel/test-routes/source/start').status_code == 200
#    assert client.post('/channel/test-routes/source/stop').status_code == 200
#
#    assert client.delete('/channel/test-routes', data='hard_delete=true').status_code == 200
