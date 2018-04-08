import pytest

import rb_backend

def test_dockerSource(app):
   with app.app_context():
      test_source = rb_backend.channel.source.dockerSource.DockerSource('test')
      assert test_source.status() == 'created'
      container = test_source._get()
      assert container.name == 'radiobretzel_tests_source_test'
      assert test_source.start()
      assert test_source.status() == 'running'
      assert test_source.stop()
      assert test_source.status() == 'exited'
      assert test_source.delete()
      with pytest.raises(rb_backend.errors.DockerError, message="source not found"):
         test_source._get()
      assert not test_source._get(silent=True)

def test_dockerSource_force_delete(app):
   with app.app_context():
      test_source = rb_backend.channel.source.dockerSource.DockerSource('test-force-rm')
      test_source.start()
      with pytest.raises(rb_backend.errors.DockerError, message="Couldn't delete source container : source is running. Use force arg to force deletion"):
         test_source.delete()
      assert test_source.delete(force=True)

def test_dockerSource_already_exists(app):
   with app.app_context():
      test_source = rb_backend.channel.source.dockerSource.DockerSource('test-exists')
      assert test_source.create(override=True)
      with pytest.raises(rb_backend.errors.DockerError, message="Couldn't create source container : container 'radiobretzel_tests_source_test' already exists"):
         test_source.create()
      test_source.delete(force=True)
