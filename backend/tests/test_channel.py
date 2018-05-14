# import pytest
#
# import rb_backend
#
# def test_Channel(app):
#    with app.app_context():
#       test_channel = rb_backend.channel.model.Channel('test-channel', **{
#          'description': 'This is a nice description',
#       })
#       assert test_channel.name == 'Test Channel'
#       assert test_channel.active == True
#       assert test_channel.soft_deleted == False
#       assert test_channel.description == 'This is a nice description'
#       assert test_channel.source.name == 'radiobretzel_tests_source_test-channel'
#       assert test_channel.source.stream_mountpoint == 'test-channel'

# def test_Channels_model(app):
#    with app.app_context():
#       test_channel = rb_backend.channel.model.Channels.create('test-channel-model')
#       test_channel = rb_backend.channel.model.Channels.update(test-channel, {'description': 'This is a nicer description'})
#       assert channel.description == 'This is a nicer description'
#       soft_deleted_channel = rb_backend.channel.model.Channels.delete('test-model')
#       assert soft_deleted_channel.soft_deleted == True
#       with pytest.raises(rb_backend.errors.DatabaseError) as e:
#          rb_backend.channel.model.Channels.find_one('test-model')
#       rb_backend.channel.model.Channels.find_one('test-model', **{'soft_deleted': 'true'})
#       rb_backend.channel.model.Channels.delete('test-model', hard_delete='true')
#       assert rb_backend.source.model.Sources.find_one(**{'mountpoint': 'ladida'})
