import pytest

import rb_backend

def test_check_length():
   rb_backend.utils.validations.check_length('This is a nice test', 128, 4)
   with pytest.raises(rb_backend.errors.ValidationError):
      rb_backend.utils.validations.check_length('Doudou', 4)
   with pytest.raises(rb_backend.errors.ValidationError):
      rb_backend.utils.validations.check_length('Doudou', 16, 14)


def test_check_mandatories():
   set = {
      'key1': 'value',
      'key2': 'value',
      'key3': 'value'
   }
   rb_backend.utils.validations.check_mandatories(set, *['key1', 'key2'])
   set.pop('key2')
   with pytest.raises(rb_backend.errors.ValidationError):
      rb_backend.utils.validations.check_mandatories(set, *['key1', 'key2', 'key3'])

def test_uuid():
   rb_backend.utils.validations.uuid('9eee1736-3529-4bc2-a0cc-24ee3cec2e0f')
   with pytest.raises(rb_backend.errors.ValidationError):
      rb_backend.utils.validations.uuid('Not a Valid UUID')

def test_slug():
   assert rb_backend.utils.validations.slug('this-is-slug') == 'this-is-slug'
   with pytest.raises(rb_backend.errors.ValidationError):
      rb_backend.utils.validations.slug('Not a good Slug')

def test_text():
   assert rb_backend.utils.validations.text("This is a nice text which will serve as an example here <>") == "This is a nice text which will serve as an example here &lt;&gt;"

def test_bool():
   assert rb_backend.utils.validations.bool('FALSE') == False
   with pytest.raises(rb_backend.errors.ValidationError):
      rb_backend.utils.validations.bool('Tarte')

def test_url():
   assert rb_backend.utils.validations.url('https://my.icecast.server/mountpoint')
   with pytest.raises(rb_backend.errors.ValidationError):
      rb_backend.utils.validations.url('ftp://lalal')
