import pytest

import rb_backend

def test_Channel(app):
   with app.app_context():
      test_channel = rb_backend.channel.model.Channel('test-channel')
      assert test_channel.name == 'Test Channel'
