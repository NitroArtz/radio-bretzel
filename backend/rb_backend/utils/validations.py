import re, html

from rb_backend.errors import ValidationError

def check_length(item, max=128, min=1):
   if len(item) > max:
      raise ValidationError('item is too long (max ' + str(max) + ' characters)')
   if len(item) <= min:
      raise ValidationError('item is too short (min ' + str(min) + ' characters)')

def check_mandatories(data, *fields):
   missings = []
   if fields:
      for key in fields:
         if key not in data.keys():
            missings.append(key)
   if not missings: return True
   raise ValidationError('missing mandatory items : '+ str(missings))

def uuid(item):
   item = html.escape(item)
   if not re.match('^[0-9A-F]{8}-[0-9A-F]{4}-[4][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$', item, re.IGNORECASE):
      raise ValidationError("item doesn't match requirements (not a valid uuid)")
   return item

def slug(item, max_length=32):
   check_length(item, max=max_length)
   item = html.escape(item)
   if not re.match('^([a-z][a-z0-9]*)((?:-[a-z0-9]+){0,2})$', item):
      raise ValidationError('item doesn\'t match requirements (only letters, digits and maximum two dashes. Cannot start with a dash.)')
   return item

def text(item, max_length=1024):
   item = html.escape(item)
   check_length(item, max=max_length)
   return item

def bool(item):
   """ Returns True or False depending on item's value (string) """
   item = html.escape(item)
   if item.lower() == 'true': return True
   if item.lower() == 'false': return False
   raise ValidationError('item is not booleean')

def url(item, max_length=128, min_length=4):
   item = html.escape(item)
   check_length(item, max=max_length, min=min_length)
   if not re.match('^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$', item):
      raise ValidationError("item is not a valid url")
   return item
