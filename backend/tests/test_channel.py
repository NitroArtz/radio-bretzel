import pytest

import rb_backend

def test_Channel(app):
   with app.app_context():
      test_channel = rb_backend.channel.model.Channel('test-channel', **{
         'description': 'This is a nice description',
         'source_args': {
            'name': 'radiobretzel_tests_source_test-channel-class',
            'stream_mountpoint': 'test-channel-override'
         },
         'force_source_creation': 'true'
      })
      assert test_channel.name == 'Test Channel'
      assert test_channel.description == 'This is a nice description'
      assert test_channel.source.name == 'radiobretzel_tests_source_test-channel-class'
      assert test_channel.source_args['stream_mountpoint'] == 'test-channel-override'

def test_channel_validations():
   set1 = {
      'uuid': '98e6bc94-87a7-41e8-9bac-830faf096b66',
      'slug': 'slug-ok',
      'name': 'Clean Name Bruh',
      'active': 'false',
      'source_name': 'jeez',
      'source_stream_mountpoint': 'sambaa'
   }
   valids = rb_backend.channel.model.Channels.validate(**set1)
   assert valids.get('uuid') == set1['uuid']
   assert valids.get('slug') == set1['slug']
   assert valids.get('name') == set1['name']
   assert valids.get('active') == False
   assert valids.get('source') == {
      'name': 'jeez',
      'stream_mountpoint': 'sambaa'
   }
   set2 = {
      'slug': 'slug isnt ok',
      'source_name': 'source name either'
   }
   with pytest.raises(rb_backend.errors.ValidationError) as e:
      invalids = rb_backend.channel.model.Channels.validate(**set2)
      # Test invalids fields here

def test_Channels_model(app):
   with app.app_context():
      rb_backend.channel.model.Channels.create('test-model')
      soft_deleted_channel = rb_backend.channel.model.Channels.delete('test-model')
      assert soft_deleted_channel.soft_deleted == True
      with pytest.raises(rb_backend.errors.DatabaseError) as e:
         rb_backend.channel.model.Channels.find_one('test-model')
      rb_backend.channel.model.Channels.find_one('test-model', **{'soft_deleted': 'true'})
      rb_backend.channel.model.Channels.delete('test-model', hard_delete='true')
