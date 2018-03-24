import re

def slug(slug):
   if len(slug) > 64:
      raise ValueError('slug is too long (max 64 characters)')
   elif not re.match('^(([a-z][a-z0-9]*))((?:-[a-z0-9]+){0,2})$', slug):
      raise ValueError('slug doesn\'t match requirements (max 64 characters, only letters, digits and maximum two dashes. Cannot start with a dash.)')
   else:
      return True
