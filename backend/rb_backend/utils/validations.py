import re

from rb_backend.errors import ValidationError

def check_length(item, max, min=1):
   if len(item) > max:
      raise ValidationError('item is too long (max ' + str(max) + ' characters)')
   if len(item) <= min:
      raise ValidationError('item is too short (min ' + str(min) + ' characters)')

def check_mandatories(data, *fields):
   missings = []
   if fields:
      for key in fields:
         if not hasattr(data, key):
            missings.append(key)
   if not missings: return False
   raise ValidationError('missing mandatory items : '+ str(missing))

def uuid(item):
   if not re.match('^[0-9A-F]{8}-[0-9A-F]{4}-[4][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$', item, re.IGNORECASE):
      raise ValidationError("item doesn't match requirements (not a valid uuid)")
   return item

def slug(item, max_length=32):
   check_length(item, max_length)
   if not re.match('^([a-z][a-z0-9]*)((?:-[a-z0-9]+){0,2})$', item):
      raise ValidationError('item doesn\'t match requirements (only letters, digits and maximum two dashes. Cannot start with a dash.)')
   return item

def text(item, max_length=1024):
   check_length(item, max_length)
   return item

def bool(item):
   """ Returns True or False depending on item's value (string) """
   if item.lower() == 'true': return True
   if item.lower() == 'false': return False
   raise ValidationError('item is not booleean')

def url(item, max_length=128, min_length=4):
   check_length(item, min_length, max_length)
   if not re.match('^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$', item):
      raise ValidationError("item is not a valid url")
